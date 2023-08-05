import atexit
import click
import datetime
import logging
import pydoni
from os.path import isfile, join, dirname


logger = pydoni.logger_setup(name='pydoni-cli', level=logging.ERROR)


class NaturalOrderGroup(click.Group):
    """
    Control click command list order.

    Source:
        https://github.com/pallets/click/issues/513
    """
    def list_commands(self, ctx):
        return self.commands.keys()


def list_commands():
    """
    Import all click commands under current directory as local variables.
    """
    from .cli_app import app
    from .cli.commands.cli_audio import cli_audio
    from .cli.commands.cli_data import cli_data
    from .cli.commands.cli_image import cli_image
    from .cli.commands.cli_imessage import cli_imessage
    from .cli.commands.cli_movie import cli_movie
    from .cli.commands.cli_opsys import cli_opsys
    from .cli.commands.cli_photo import cli_photo
    from .cli.commands.cli_video import cli_video

    # CLI commands that may or may not be ignored
    if isfile(join(dirname(__file__), 'cli', 'commands', 'cli_notes.py')):
        from .cli.commands.cli_notes import cli_notes

    return locals()


def add_commands(cl_commands):
    """
    Add them to `cli` function object. This will allow the `doni` commandline call
    visibility to all click commands housed under the current directory.
    """
    for cmd_name, cmd_obj in cl_commands.items():
        cli.add_command(cmd_obj)


def update_database_backend(schema_name, table_name, start_ts):
    """
    Update backend command history table. This table can be updated each time a `pydoni`
    command is run.
    """
    logger.info(f'Appending a record to command history table {schema_name}.{table_name}')
    pg = pydoni.Postgres()

    end_ts = datetime.datetime.utcnow()

    def get_pydoni_attr(attr_name):
        if hasattr(pydoni, attr_name):
            attr_value = getattr(pydoni, attr_name)
            return str(attr_value) if attr_value is not None else 'NULL'
        else:
            return 'NULL'

    e = get_pydoni_attr('pydonicli_e')
    args = get_pydoni_attr('pydonicli_args')
    result = get_pydoni_attr('pydonicli_result')
    command_name = get_pydoni_attr('pydonicli_command_name')

    if command_name == 'NULL':
        logger.warning(pydoni.advanced_strip("""Expected variable `pydoni.pydonicli_command_name`
        not found, command history log not updated"""))

    else:
        elapsed_sec = datetime.datetime.timestamp(end_ts) - datetime.datetime.timestamp(start_ts)

        columns_values = [
            ('command_name', command_name),
            ('start_ts', start_ts),
            ('end_ts', end_ts),
            ('elapsed_sec', elapsed_sec),
            ('error_msg', e),
            ('args', args),
            ('result', result),
        ]

        if 'pg' in locals() or 'pg' in globals():
            insert_sql = pg.build_insert(schema_name=schema_name,
                                        table_name=table_name,
                                        columns=[col for col, val in columns_values],
                                        values=[val for col, val in columns_values],
                                        validate=True)
            pg.execute(insert_sql)
        else:
            logger.warning(f'No connection to database backend established. No record inserted to {schema_name}.{table_name}')


@click.group(cls=NaturalOrderGroup)
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Change logging level to INFO.')
@click.option('--log/--no-log', is_flag=True, default=True,
              help='Trigger a command history update on exit to a backend Postgres database.')

def cli(verbose, log):
    """
    Command line interface to `pydoni` module.
    """
    global start_ts
    start_ts = datetime.datetime.utcnow()

    logging_level = logging.INFO if verbose else logging.ERROR
    logger.setLevel(logging_level)
    pydoni.module_loglevel = logging_level

    if log:
        atexit.register(update_database_backend, 'pydonicli', 'command_history', start_ts)


def main(args=None):
    add_commands(list_commands())
    try:
        cli()
    except Exception as e:
        error = e
        pydoni.pydonicli_e = str(error)

    if 'error' in locals():
        raise error
