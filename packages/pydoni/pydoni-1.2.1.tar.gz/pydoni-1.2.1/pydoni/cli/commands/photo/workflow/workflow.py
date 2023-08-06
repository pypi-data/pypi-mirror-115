import click
import pydoni
import re
import time
from ...common import Verbose
from .db_transform import db_transform
from .source_to_postgres_pipeline import source_to_postgres_pipeline
from clint.textui import colored
from os.path import splitext, getmtime, basename, getsize, isfile, join, dirname
from pyfiglet import Figlet
from send2trash import send2trash


def print_startup_message():
    """
    Print startup message to console.
    """
    tab = '    '  # This is used in `msg_fmt` format string
    fig = Figlet(font='slant')

    print(colored.red(fig.renderText('Photo ELT')))
    print()

    with open(join(dirname(__file__), 'verbosity', 'startup_message.txt'), 'r') as f:
        msg = f.read()
        msg_fmt = eval("f'''{}'''".format(msg))
        msg_lst = msg_fmt.split('\n')
        for line in msg_lst:
            print(line)
            time.sleep(.01)

        time.sleep(1)


@click.option('--source-dpath', type=click.Path(exists=False),
              help='Path containing source mediafiles.')
@click.option('--pg-schema', type=str, default='photo',
              help='Existing Postgres Photo schema name.')
@click.option('--sample', type=int, default=None,
              help='Randomly sample this many files to run through the pipeline. Primarily for testing.')
@click.option('--full-rebuild', is_flag=True, default=False,
              help='Fully rebuild every Photo table in Postgres.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')
@click.option('--dry-run', is_flag=True, default=False,
              help='Do not insert any data to Postgres database.')
@click.option('--no-startup-message', is_flag=True, default=False,
              help='Do not print Workflow ELT startup message.')
@click.option('--no-pipeline', is_flag=True, default=False,
              help=re.sub(r'\s+', '', '''Do not read source media files and pipe metadata to Postgres. Instead, simply execute the portion of the workflow that occurs after
              the data pipeline is normally complete. Enabling this option lifts the
              restriction that `source_dpath` must be an available directory.'''))


@click.command()
def workflow(source_dpath,
             pg_schema,
             sample,
             full_rebuild,
             verbose,
             dry_run,
             no_startup_message,
             no_pipeline):
    """
    Refresh Postgres Photo schema from source photo metadata.
    """
    args = pydoni.__pydonicli_declare_args__(locals())
    pydoni.__pydonicli_register__({'command_name': pydoni.what_is_my_name(with_modname=True), 'args': args})

    # Begin pipeline stopwatch
    start_ts = time.time()

    # Set up variables used throughout entire pipeline
    vb = Verbose(verbose)
    pg = pydoni.Postgres()

    if vb.verbose:
        if not no_startup_message:
            print_startup_message()

    # Extract source media file metadata and load into Postgres
    pipeline_args = dict(pg=pg,
                         vb=vb,
                         source_dpath=source_dpath,
                         pg_schema=pg_schema,
                         sample=sample,
                         full_rebuild=full_rebuild)

    if not no_pipeline:
        source_to_postgres_pipeline(**pipeline_args)

    # Apply transformations on data once loaded into Postgres
    db_transform(pg, vb, pg_schema, sample)

    # End workflow
    pydoni.__pydonicli_register__({k: v for k, v in locals().items() if k in ['result']})
    msg = f'Photo database refresh complete'
    vb.program_complete(msg, start_ts=start_ts)
