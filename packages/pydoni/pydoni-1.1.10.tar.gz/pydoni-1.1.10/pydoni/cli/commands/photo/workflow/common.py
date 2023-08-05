import click
import pydoni
import ast
from os.path import join, dirname, splitext, isfile


title_border_left = '->->->->->->->->->->->->->'
title_border_right = '<-<-<-<-<-<-<-<-<-<-<-<-<-'

table_schemas_dpath = join(dirname(__file__), 'database_objects', 'table_schemas')
view_schemas_dpath = join(dirname(__file__), 'database_objects', 'view_schemas')


class StagedTable(object):
    """
    Store data for a staged table in the Postgres database.
    """
    def __init__(self, table_schema, table_name):
        self.table_schema = table_schema
        self.table_name = table_name
        self.columnspec = read_staged_table_schema(table_name)


def format_text(string, fmt=None):
    """
    Format a text string according to pre-defined presets.
    """
    string = str(string)
    fmt = str(fmt).lower()

    if fmt == 'title':
        return click.style(string, bold=True)
    elif fmt in ['code', 'path']:
        return click.style(string, fg='black')
    else:
        return string


def read_staged_table_schema(table_name):
    """
    Search in the table schemas directory for the named JSON file, and read
    the specified column specification as a list of tuples.
    """
    schema_fpath = join(table_schemas_dpath, table_name + '.json')

    with open(schema_fpath, 'r') as f:
        json_txt = f.read()
        columnspec = ast.literal_eval(json_txt)
        columnspec = [(k, v) for k, v in columnspec.items()]

    return columnspec


def list_views():
    """
    List all views by name (filename without extension) in the expected directory.
    """
    view_fpaths = pydoni.listfiles(view_schemas_dpath, ext='sql')
    return [splitext(basename(x))[0] for x in view_fpaths]


def find_view(view_name):
    """
    Search in the view schemas directory for the named SQL file.
    """
    schema_fpath = join(view_schemas_dpath, view_name + '.sql')
    assert isfile(schema_fpath), f"Unable to find view '{view_name}' in directory '{view_schemas_dpath}'"
    return schema_fpath


def define_view(pg, view_name):
    """
    Search in the view schemas directory for the named SQL file, and execute
    the specified SQL.
    """
    schema_fpath = find_view(view_name)

    with open(schema_fpath, 'r') as f:
        sql_text = f.read()
        pg.execute(sql_text)


def define_all_views(pg):
    """
    List and define all views with definitions in the expected directory.
    """
    view_lst = list_views()
    for vw_name in view_lst:
        define_view(pg, vw_name)
