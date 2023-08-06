import emoji
import pandas as pd


def refresh_emoji_text_map(pg, vb, tag, dry_run, table_schema, table_name):
    """
    Rebuild a table in Postgres mapping emoji characters with their plain
    text names formatted between colons (i.e. :1st_place_medal:).
    """
    result = {}

    emoji_table = pd.DataFrame(emoji.UNICODE_EMOJI['en'], index=[0])
    emoji_table = emoji_table.T.reset_index().rename(columns={'index': 'emoji', 0: 'plain_text'})

    result['n_emoji'] = len(emoji_table)
    vb.info(f'Generated table of emojis from `emoji` package, shape: {emoji_table.shape}', tag=tag)

    if not dry_run:
        emoji_table.to_sql(name=table_name,
                           con=pg.dbcon,
                           schema=table_schema,
                           index=False,
                           if_exists='append')
    else:
        tag.add('dry-run')

    vb.info(f'Refreshed table {table_schema}.{table_name}', tag=tag)

    return result