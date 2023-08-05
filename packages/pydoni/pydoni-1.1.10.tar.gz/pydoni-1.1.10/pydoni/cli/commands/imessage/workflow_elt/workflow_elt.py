import click
import pydoni
import sqlite3
import time
from ...common import Verbose
from .extract import extract_sqlite
from .load import load_postgres
from .transform import transform
from clint.textui import colored
from collections import OrderedDict
from os.path import expanduser, dirname, join
from pyfiglet import Figlet


def print_startup_message():
    """
    Print startup message to console.
    """
    tab = '    '  # This is used in `msg_fmt` format string
    fig = Figlet(font='slant')

    print(colored.red(fig.renderText('iMessage ELT')))
    print()

    with open(join(dirname(__file__), 'elt_logging', 'startup_message.txt'), 'r') as f:
        msg = f.read()
        msg_fmt = eval("f'''{}'''".format(msg))
        msg_lst = msg_fmt.split('\n')
        for line in msg_lst:
            print(line)
            time.sleep(.02)

        time.sleep(2)


@click.option('--chat-db-path', type=str, default=expanduser('~/Library/Messages/chat.db'),
              help='Path to working chat.db.')
@click.option('--pg-schema-load', type=str, default='imessage_current',
              help='Existing Postgres iMessage schema name.')
@click.option('--pg-schema-live', type=str, default='imessage',
              help='Existing Postgres iMessage schema name.')
@click.option('--full-refresh', is_flag=True, default=False,
              help='Fully rebuild every iMessage table in Postgres.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')
@click.option('--dry-run', is_flag=True, default=False,
              help='Do not insert any data to Postgres database.')
@click.option('--no-startup-message', is_flag=True, default=False,
              help='Do not print Workflow ELT startup message.')
@click.command()
def workflow_elt(chat_db_path,
                 pg_schema_load,
                 pg_schema_live,
                 full_refresh,
                 verbose,
                 dry_run,
                 no_startup_message):
    """
    Fully refresh Postgres iMessage schema from local SQLite chat.db.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    # Begin pipeline stopwatch
    start_ts = time.time()

    # Set up variables used throughout entire pipeline
    vb = Verbose(verbose)
    pg = pydoni.Postgres()

    try:
        sqlite_con = sqlite3.connect(chat_db_path)
    except Exception as e:
        raise(Exception(pydoni.advanced_strip("""Unable to connect to SQLite! Could it be
        that the executing environment does not have proper permissions? Perhaps wrapping
        the command in an application or script, and granting Full Disk Access to that
        application or script might be a potential option""")))

    if vb.verbose:
        if not no_startup_message:
            print_startup_message()

    # Returns a SQLiteiMessageDatabaseExtract object containing a list of
    # SQLiteiMessageTable objects
    chat_db_extract = extract_sqlite(pg=pg,
                                     vb=vb,
                                     chat_db_path=chat_db_path,
                                     sqlite_con=sqlite_con,
                                     pg_schema=pg_schema_load,
                                     full_refresh=full_refresh)

    # Load data into Postgres database
    load_postgres(pg=pg,
                  vb=vb,
                  chat_db_extract=chat_db_extract,
                  pg_schema_load=pg_schema_load,
                  pg_schema_live=pg_schema_live,
                  dry_run=dry_run,
                  full_refresh=full_refresh)

    # Apply Transform steps on data loaded into Postgres with full access
    # to custom views and staged tables
    transform_result = transform(pg=pg,
                                 vb=vb,
                                 pg_schema_load=pg_schema_load,
                                 pg_schema_live=pg_schema_live,
                                 full_refresh=full_refresh,
                                 dry_run=dry_run)

    # Extract dictionary of information from `chat_db_extract` for logging
    chat_db_info = OrderedDict()
    for tobject in chat_db_extract.table_objects:
        name = tobject.sqlite_table_name
        ignore_keys = ['df', 'sqlite_table_name']
        chat_db_info[name] = {k: v for k, v in tobject.__dict__.items() if k not in ignore_keys}

    # Combine pipeline step results into one comprehensive dictionary
    new_messages_processed = chat_db_info['message']['shape'][0]
    result = dict(extract=chat_db_info, transform=transform_result)
    result['new_messages_processed'] = new_messages_processed

    # End pipeline
    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='imessage.workflow_elt'))
    plural = '' if new_messages_processed == 1 else 's'
    msg = f'iMessage ELT complete ({new_messages_processed} message{plural} processed)'
    vb.program_complete(msg, start_ts=start_ts)
