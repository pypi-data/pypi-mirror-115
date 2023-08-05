import click
import pandas as pd
from .elt_logging.elt_logging import ColorTag


class SQLiteiMessageTable(object):
    """
    Store data from a single table in chat.db.
    """
    def __init__(self, df, sqlite_table_name, write_mode):
        self.df = df
        self.shape = df.shape
        self.sqlite_table_name = sqlite_table_name
        self.write_mode = write_mode


class SQLiteiMessageDatabaseExtract(object):
    """
    Store list of chat.db table objects.
    """
    def __init__(self):
        self.table_objects = []

    def add_table(self, table_object):
        """
        Append a SQLiteiMessageTable object to `self.table_objects`.
        """
        self.table_objects.append(table_object)


def extract_sqlite(pg, vb, chat_db_path, sqlite_con, pg_schema, full_refresh):
    """
    Query SQLite database for iMessage tables, and filter for records not already in
    the Postgres database mirrored tables.

    For example if this workflow was run 1hr ago, only extract the last hour's worth of
    iMessage data from SQLite, rather than for all time.
    """
    vb.info(f"->->->->->->->->->->->->-> {click.style('Extract', bold=True)} <-<-<-<-<-<-<-<-<-<-<-<-<-")
    tag = ColorTag()

    # Connect to SQLite chat.db
    sqlite_cursor = sqlite_con.cursor()
    vb.info(f'Connected to SQLite database: {chat_db_path}')

    # Get full list of SQLite tables in DB
    sqlite_cursor.execute("select name from sqlite_master where type = 'table';")
    sqlite_tables = [x[0] for x in sqlite_cursor.fetchall()]

    if full_refresh:
        tag.add('full-refresh')
        vb.info('Rebuilding Postgres database from scratch (option --full-refresh ON)', tag=tag)
        append_table_dict = dict()
    else:
        # Table name : join column pairs
        append_table_dict = dict(
            chat_message_join=['chat_id', 'message_id'],
            attachment='ROWID',
            message='ROWID',
            message_attachment_join=['message_id', 'attachment_id'])

    chat_db_extract = SQLiteiMessageDatabaseExtract()

    # Extract all rows for tables not specified in `append_table_dict`.
    # These tables will be fully rebuilt in Postgres (wipe all rows then insert).
    vb.info('Reading chat.db source tables...', bold=True)
    for tname in [x for x in sqlite_tables if x not in append_table_dict.keys()]:
        df_sqlite = pd.read_sql(f'select * from {tname}', sqlite_con)
        tobject = SQLiteiMessageTable(df_sqlite, sqlite_table_name=tname, write_mode='overwrite')
        chat_db_extract.add_table(tobject)
        vb.info(f"SQLite:{click.style(tname, fg='black')}, shape: {df_sqlite.shape}", arrow='white')

    # Extract only new records for tables specified in `append_table_dict`
    for tname, join_cols in append_table_dict.items():
        df_sqlite = pd.read_sql(f'select * from {tname}', sqlite_con)

        if pg.table_exists(pg_schema, tname):
            existing_table = pg.read_table(pg_schema, tname)
            outer_join = df_sqlite.merge(existing_table[join_cols],
                                         how='outer',
                                         left_on=join_cols,
                                         right_on=join_cols,
                                         indicator=True)

            df_sqlite = (outer_join[outer_join['_merge'] == 'left_only']
                         .drop('_merge', axis=1)
                         .drop_duplicates())

        tobject = SQLiteiMessageTable(df_sqlite, sqlite_table_name=tname, write_mode='append')
        chat_db_extract.add_table(tobject)

        if len(df_sqlite):
            vb.info(f"SQLite:{click.style(tname, fg='black')}, shape: {df_sqlite.shape}", arrow='white')
        else:
            vb.warn(f'No new records found in SQLite:{tname} that are not already in Postgres:{pg_schema}.{tname}', arrow='yellow')

    vb.info('iMessage data successfully extracted from SQLite ✔️', bold=True)
    return chat_db_extract
