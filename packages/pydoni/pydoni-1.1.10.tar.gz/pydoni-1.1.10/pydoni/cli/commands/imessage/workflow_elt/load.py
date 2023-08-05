import click
import pandas as pd
import pydoni
from os.path import join, dirname
from .db_views.db_views import drop_views
from .elt_logging.elt_logging import ColorTag


def drop_all_imessage_schema_objects(pg, vb, pg_schema_load, pg_schema_live, dry_run):
    """
    WARNING: This function is only intended for use when the `full_refresh` option is on.

    Drop all tables and views in the target iMessage schema, according to the following protocol:

        1. Drop all views with `cascade` option on to avoid view dependency errors being thrown.
        2. Drop all chat.db tables that exist in Postgres.
        3. Drop all user staged tables.
    """
    if not dry_run:
        drop_views(pg, vb, pg_schema_load, dry_run, verbose=False)
        drop_views(pg, vb, pg_schema_live, dry_run, verbose=False)

        load_tables = pg.list_tables(table_schema=pg_schema_load)
        for _, row in load_tables.iterrows():
            pg.execute(f"drop table if exists {row['table_schema']}.{row['table_name']}")

        live_tables = pg.list_tables(table_schema=pg_schema_live)
        for _, row in live_tables.iterrows():
            pg.execute(f"drop table if exists {row['table_schema']}.{row['table_name']}")


def create_mapping_tables_if_not_exist(pg, vb, pg_schema_load, full_refresh, dry_run):
    """
    Create mapping tables in `load` schema if not already created. These tables are
    architectural mapping tables not included in chat.db that are necessary
    for joining historical chat.db versions and maintaining a unique message
    identifier (`message_uid`) across those versions of chat.db.
    """
    tag = ColorTag()

    mapping_tables = [
        (pg_schema_load, 'map_attachment_id'),
        (pg_schema_load, 'map_chat_id'),
        (pg_schema_load, 'map_handle_id'),
        (pg_schema_load, 'map_message_id'),
    ]

    mapping_table_columnspec = [
        ('ROWID', 'bigint'),
        ('source', 'text'),
    ]

    for s, t in mapping_tables:
        exists = pg.table_exists(s, t)
        if full_refresh or not exists:
            if not dry_run:
                pg.execute(f'drop table if exists {s}.{t} cascade')
                pg.execute(f'drop sequence if exists {s}.{t}_seq')
                pg.execute(f'create sequence {s}.{t}_seq')

                id_col_dtype = f"int8 not null default id_generator((nextval('{s}.{t}_seq'::regclass))::integer)"
                columnspec = [(t.replace('map_', '').replace('_id', '_uid'), id_col_dtype)] + mapping_table_columnspec
                pg.create_table(table_schema=s, table_name=t, columnspec=columnspec)
                pg.execute(f'alter table {s}.{t} rename column "rowid" to "ROWID"')

            if not exists:
                vb.info(f"Created empty mapping table as it didn't previously exist {click.style(s + '.' + t, fg='black')}", arrow='white')
            else:
                # Must have re-created because of full_refresh`
                tag.add('full-refresh')
                vb.warn(f"Re-created empty mapping table {click.style(s + '.' + t, fg='black')}", arrow='white', tag=tag)


def load_chat_db_tables(pg, vb, chat_db_extract, pg_schema_load, dry_run):
    """
    Load chat.db tables into Postgres.
    """
    tag = ColorTag()

    for tobject in chat_db_extract.table_objects:
        if not dry_run:
            write_mode = 'replace' if tobject.write_mode == 'overwrite' else tobject.write_mode
            if write_mode == 'replace':
                pg.execute(f'drop table if exists {pg_schema_load}.{tobject.sqlite_table_name} cascade')

            tobject.df.to_sql(name=tobject.sqlite_table_name,
                              con=pg.dbcon,
                              schema=pg_schema_load,
                              index=False,
                              if_exists=write_mode)
        else:
            tag.add('dry-run')

        if len(tobject.df):
            if tobject.write_mode == 'overwrite':
                msg = f"""
                Rebuilt
                Postgres:{click.style(tobject.sqlite_table_name, fg='black')}
                with data from
                SQLite:{click.style(tobject.sqlite_table_name, fg='black')}
                """
            else:
                msg = f"""
                Appended {len(tobject.df)} new records from
                SQLite:{click.style(tobject.sqlite_table_name, fg='black')}
                to
                Postgres:{click.style(tobject.sqlite_table_name, fg='black')}
                """

            vb.info(msg, arrow='white', tag=tag)


def load_manual_tables(pg, vb, pg_schema_load, pg_schema_live, dry_run):
    """
    Load each indiviudal manually maintained table to Postgres. Each table will require
    its own protocol, detailed in this function.
    """
    tag = ColorTag()

    # First execute SQL table definitions. This SQL script may drop and re-create some
    # tables that are designed to be re-created by this workflow automatically
    with open(join(dirname(__file__), 'manual_tables', 'manual_table_defs.sql'), 'r') as f:
        manual_table_def_sql = f.read()
        if not dry_run:
            pg.execute(manual_table_def_sql)
        else:
            tag.add('dry-run')

        vb.info('Executed manual table defintions', arrow='white', tag=tag)

    # Now populate individual tables in Postgres
    table_data = dict()
    table_data[0] = dict(
        table_schema=pg_schema_live,
        table_name='contact_names_ignored',
        fpath=join(dirname(__file__), 'manual_tables', 'table_data', 'contact_names_ignored.csv')
    )
    table_data[1] = dict(
        table_schema=pg_schema_live,
        table_name='contact_names_manual',
        fpath=join(dirname(__file__), 'manual_tables', 'table_data', 'contact_names_manual.csv')
    )

    for k, v in table_data.items():
        v['df'] = pd.read_csv(v['fpath'])

        # Query the existing table and get its shape. Raise an error if the Postgres
        # table has more rows than the local .csv that it's being replaced with, as this
        # scenario would indicate that the user edited the Postgres table out of band.
        existing_table = pg.read_table(v['table_schema'], v['table_name'])
        if v['df'].shape[0] < existing_table.shape[0]:
            raise Exception(pydoni.advanced_strip("""
            Table {v['table_schema']}.{v['table_name']} is maintained via a local .csv
            file in this workflow, but the Postgres table has more records than the
            local .csv file that it will be replaced with. Has the table been manually
            edited out of band? Make sure there are no extra records in the Postgres table
            that are not in the file "{v['fpath']}". When that is complete, delete
            the Postgres table with "drop table {v['table_schema']}.{v['table_name']} cascade;",
            then re-run the workflow.
            """).strip())

        if not dry_run:
            v['df'].to_sql(name=v['table_name'],
                           con=pg.dbcon,
                           schema=v['table_schema'],
                           index=False,
                           if_exists='replace')

        vb.info(f"""
        Refreshed table
        {click.style(v['table_schema'] + '.' + v['table_name'], fg='black')}
        """, arrow='white', tag=tag)


def append_new_rowids_to_map_tables(pg, vb, dry_run, pg_schema_load):
    """
    Execute SQL against the Postgres database to keep the map_*_id tables up to date. These
    tables map the generic iMessage "ROWID" to a truly unique identifier, generated within
    the Postgres database.
    """
    tag = ColorTag()
    result = {}

    sqlfile = join(dirname(__file__), 'data_quality', 'append_new_rowids_to_map_tables.sql')
    with open(sqlfile, 'r') as f:
        sql = f.read().format(**locals())

    if not dry_run:
        pg.execute(sql)
    else:
        tag.add('dry-run')

    msg = 'Appended new attachment, chat, handle or message ROWID values to map_*_id tables'
    vb.info(msg, arrow='white', tag=tag)

    return result


def load_postgres(pg, vb, chat_db_extract, pg_schema_load, pg_schema_live, dry_run, full_refresh):
    """
    Accept a SQLiteiMessageDatabaseExtract object and load each table into Postgres.
    """
    vb.info(f"->->->->->->->->->->->->-> {click.style('Load', bold=True)} <-<-<-<-<-<-<-<-<-<-<-<-<-")
    tag = ColorTag()

    if full_refresh:
        tag.add('full-refresh')
        drop_all_imessage_schema_objects(pg, vb, pg_schema_load, pg_schema_live, dry_run)
        vb.info('Dropped all views and tables in schema', tag=tag)
        tag.remove('full-refresh')
    else:
        drop_views(pg, vb, pg_schema_load, dry_run, verbose=2)

    vb.info(f"Ensuring architectural ID mapping tables exist in schema {click.style(pg_schema_load, fg='black')}...", bold=True)
    create_mapping_tables_if_not_exist(pg, vb, pg_schema_load, full_refresh, dry_run)

    vb.info(f"Loading physicalized chat.db tables to schema {click.style(pg_schema_load, fg='black')}...", bold=True)
    load_chat_db_tables(pg, vb, chat_db_extract, pg_schema_load, dry_run)

    vb.info(f'Populating new mapping IDs...', bold=True)
    append_new_rowids_to_map_tables(pg, vb, dry_run, pg_schema_load)

    vb.info(f'Refreshing manually maintained tables...', bold=True)
    load_manual_tables(pg, vb, pg_schema_load, pg_schema_live, dry_run)

    vb.info('iMessage data successfully loaded into Postgres database ✔️', bold=True)
