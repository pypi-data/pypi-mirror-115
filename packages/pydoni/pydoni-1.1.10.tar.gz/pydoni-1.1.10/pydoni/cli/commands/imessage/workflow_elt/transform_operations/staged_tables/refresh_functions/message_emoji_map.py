import pandas as pd
import numpy as np
from tqdm import tqdm


def refresh_message_emoji_map(pg, vb, tag, dry_run, table_schema, table_name, emoji_table):
    """
    Refresh or rebuild a table in Postgres mapping messages to a boolean columns indicating
    whether that message contains an emoji.
    """
    result = {}

    emoji_table = pg.read_table(emoji_table.table_schema, emoji_table.table_name)
    emoji_lst = emoji_table['emoji'].tolist()
    vb.info(f'Read emoji table, shape: {emoji_table.shape}', tag=tag)

    messages = pg.read_sql(f"""
    select
        m.message_uid::text
        , m."text"
    from
        imessage.message_vw m
    left join
        {table_schema}.{table_name} e
        on m.message_uid = e.message_uid
    where
        m.is_text = true
        and e.message_uid is null  -- Not in message-emoji map
    """)

    vb.info(f'Total messages without `has_emoji` flag: {len(messages)}', tag=tag)

    if vb.verbose and len(messages) > 0:
        vb.pbar = tqdm(total=np.ceil(len(messages) * 1.0 / 10), unit='message')

    vb.info('Scanning messages for emojis...', tag=tag)
    message_emoji_map = pd.DataFrame(columns=['message_uid', 'has_emoji'])
    for i, row in messages.iterrows():
        msg_has_emoji = any([em in row['text'] for em in emoji_lst])
        message_emoji_map.loc[len(message_emoji_map) + 1] = [row['message_uid'], msg_has_emoji]
        vb.pbar_update(10)

    if len(messages) > 0:  # `pbar` must have been opened
        vb.pbar_close()

    vb.info(f'Shape of message_emoji_map: {message_emoji_map.shape}', tag=tag)

    if not dry_run:
        message_emoji_map.to_sql(name=table_name,
                                 con=pg.dbcon,
                                 schema=table_schema,
                                 index=False,
                                 if_exists='append')
    else:
        tag.add('dry-run')

    vb.info(f"""Appended records to
    {table_schema}.{table_name}: {len(message_emoji_map)}""", tag=tag)

    result['n_appended_to_message_emoji_map'] = len(message_emoji_map)

    return result
