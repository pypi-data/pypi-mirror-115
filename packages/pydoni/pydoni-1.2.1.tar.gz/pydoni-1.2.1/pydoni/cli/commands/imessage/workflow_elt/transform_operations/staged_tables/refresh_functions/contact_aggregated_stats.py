import datetime
import pydoni
import pandas as pd


def refresh_contact_aggregated_stats(pg, vb, tag, dry_run, table_schema, table_name, acceptable_token_languages):
    """
    Maintain a table containing aggregated statistics by contact name (i.e. one row
    per contact name, containing stats such as total messages, earliest message date,
    most recent message date, etc.).

    Parameters:
        self (PostgresiMessageDatabaseTransform): Passed object.
        acceptable_token_languages (str): Languages to collect token statistics by contact for.
    """
    result = {}

    # Get message stats per contact
    vb.info('Computing message statistics by contact', tag=tag)

    message = pg.read_sql(f"""
    select
        message_uid
        , contact_name
        , message_date :: date as message_date
        , "text"
        , n_characters
        , n_words
        , case
              when is_from_me = true then 'from_me'
              when is_from_me = false then 'from_them'
              else null
          end as from_me_cat
    from
        imessage.message_vw
    where
        is_text = true
        and message_uid is not null
    """)

    aggregations = {
        'message_uid': pd.Series.nunique,
        'n_characters': sum,
        'n_words': sum,
        'message_date': [min, max, pd.Series.nunique],
    }

    contact_name = message.groupby('contact_name').agg(aggregations)
    contact_name = pydoni.collapse_df_columns(contact_name)

    contact_name_from_me = message.groupby(['contact_name', 'from_me_cat']).agg(aggregations)
    contact_name_from_me = pydoni.collapse_df_columns(contact_name_from_me).reset_index()

    value_columns = [x for x in contact_name_from_me.columns if x not in ['contact_name', 'from_me_cat']]
    contact_name_from_me = (
        contact_name_from_me.pivot(
            index='contact_name',
            columns='from_me_cat',
            values=value_columns))

    contact_name_from_me = pydoni.collapse_df_columns(contact_name_from_me)

    column_rename_map = {
        'message_uid_nunique': 'n_messages',
        'n_characters_sum': 'n_characters',
        'n_words_sum': 'n_words',
        'message_date_min': 'first_message_date',
        'message_date_max': 'last_message_date',
        'message_date_nunique': 'n_active_days',
    }

    for x, y in column_rename_map.items():
        new_columns = []
        for c in contact_name.columns:
            if x in c:
                new_columns.append(c.replace(x, y))
            else:
                new_columns.append(c)

        contact_name.columns = new_columns

        new_columns = []
        for c in contact_name_from_me.columns:
            if x in c:
                new_columns.append(c.replace(x, y))
            else:
                new_columns.append(c)

        contact_name_from_me.columns = new_columns

    # Get token usage stats per contact

    vb.info('Computing top token statistics by contact', tag=tag)

    contact_top_tokens_and_emojis = pg.read_sql(f"""
    with t1 as (
        select *
            , row_number() over(
                partition by contact_name, case when "language" = 'emoji' then 1 else 0 end
                order by n_token_uses desc) as r
        from
            imessage.contact_token_usage_vw
        where
            "language" in ({', '.join("'" + x + "'" for x in acceptable_token_languages)})

    )

    , t2 as (
        select *
        from t1
        where r = 1
    )

    , t3 as (
        select
            contact_name
            , "token" as top_token
            , n_token_uses as n_top_token_uses
            , n_messages_where_token_used as n_messages_where_top_token_used
            , first_use_date as top_token_first_use_date
            , last_use_date as top_token_last_use_date
        from
            t2
        where
            "language" <> 'emoji'
    )

    , t4 as (
        select
            t2.contact_name
            , t2."token" as top_emoji
            , e.plain_text as top_emoji_text
            , t2.n_token_uses as n_top_emoji_uses
            , t2.n_messages_where_token_used as n_messages_where_top_emoji_used
            , t2.first_use_date as top_emoji_first_use_date
            , t2.last_use_date as top_emoji_last_use_date
        from
            t2
            left join imessage.emoji_text_map e
                   on t2."token" = e.emoji
        where
            "language" = 'emoji'
    )

    select *
    from t3
    left join t4
        using (contact_name)
    """)

    # Combine stats into a single dataframe
    vb.info('Computing dependent aggregated columns', tag=tag)

    stats = (
        contact_name
        .merge(contact_name_from_me, on='contact_name', how='left')
        .merge(contact_top_tokens_and_emojis, on='contact_name', how='left')
    ).copy()

    # Compute dependent columns

    date_columns = [
        'first_message_date',
        'first_message_date_from_me',
        'first_message_date_from_them',
        'last_message_date',
        'last_message_date_from_me',
        'last_message_date_from_them',
        'top_emoji_first_use_date',
        'top_emoji_last_use_date',
        'top_token_first_use_date',
        'top_token_last_use_date',
    ]
    for c in date_columns:
        stats[c] = pd.to_datetime(stats[c])

    stats['n_days_from_first_to_last_message_date'] = \
        (stats['last_message_date'] - stats['first_message_date']).apply(lambda x: x.days)

    stats['pct_active_days'] = \
        1.0 * stats['n_active_days'] / stats['n_days_from_first_to_last_message_date']

    stats['pct_messages_from_me'] = 1.0 * stats['n_messages_from_me'] / stats['n_messages']
    stats['pct_messages_from_them'] = 1.0 * stats['n_messages_from_them'] / stats['n_messages']

    stats['n_days_since_last_message'] = \
        (datetime.datetime.now() - stats['last_message_date']).apply(lambda x: x.days)

    stats['n_days_since_last_reply_from_me'] = \
        (datetime.datetime.now() - stats['last_message_date_from_me']).apply(lambda x: x.days)

    stats['n_days_since_last_reply_from_them'] = \
        (datetime.datetime.now() - stats['last_message_date_from_them']).apply(lambda x: x.days)

    columns_ordered = ['contact_name'] + sorted([x for x in stats.columns if x != 'contact_name'])
    stats = stats[columns_ordered]

    vb.info(f'Re-populating {table_schema}.{table_name}', tag=tag)
    if not dry_run:
        stats.to_sql(
            name=table_name,
            con=pg.dbcon,
            schema=table_schema,
            index=False,
            if_exists='append')
    else:
        tag.add('dry-run')

    result['n_contacts_computed_stats_for'] = len(stats)
    vb.info(f'Appended records to {table_schema}.{table_name}: {len(stats)}', tag=tag)

    return result