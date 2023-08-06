import click
import pydoni
from ..elt_logging.elt_logging import ColorTag
from collections import OrderedDict
from os.path import basename, dirname, splitext, join, isfile


def drop_views(pg, vb, pg_schema, dry_run, verbose=1):
    """
    Drop all views with SQL definitions in ../db_views/. Set `verbose` to 2 to list the
    name of each view dropped.
    """
    tag = ColorTag()
    views = pg.list_views(pg_schema)['view_name']

    if dry_run:
        tag.add('dry-run')

    if len(views):
        if verbose == 2:
            vb.info('Dropping database views...', bold=True)

        for vw in views:
            if not dry_run:
                pg.execute(f'drop view if exists {pg_schema}.{vw} cascade;')

            if verbose == 2:
                vb.info(f"{click.style(pg_schema + '.' + vw, fg='black')}", arrow='white', tag=tag)

        if verbose >= 1:
            vb.info('Dropped database views (use `define_views()` to restore views to database)', tag=tag)


def define_views(pg, vb, pg_schema, verbose=1, safe=False, dry_run=False):
    """
    Execute database view definitions. Set `verbose` to 2 to list the name of each
    view created. Otherwise, simply use `vb.info()` to print to console that new views
    were created.

    fpath = full filepath
    dpath = full directory path
    fname = basename with extension
    name = basename without extension
    """
    def read_view_sqlfile(vw_fpath):
        """Read view SQL file as text."""
        with open(vw_fpath, 'r') as f:
            return f.read()


    def execute_view_def(vw_sql, vw_name, safe, verbose):
        """
        Execute view definition SQL.
        """
        if safe:
            # Only re-define a view if it doesn't throw an error
            try:
                pg.execute(vw_sql)
            except:
                return False
        else:
            # Require that the view can be defined, throw error if view definition fails
            pg.execute(vw_sql)

        if verbose == 2:
            vb.info(f'Refreshed view definition {pg_schema}.{vw_name}', arrow='white', tag=tag)

        return True


    tag = ColorTag()
    if dry_run:
        tag.add('dry-run')

    vw_sql_dpath = join(dirname(__file__), 'view_defs')
    vw_sql_fpaths = pydoni.listfiles(vw_sql_dpath, full_names=True, ext='.sql')

    if verbose == 2:
        vb.info('Re-defining database views...', bold=True, tag=tag)

    # Assign 'independent' views as those which do not depend on other views, and
    # 'dependent' views as those which do
    # TODO: Make these independent/dependent views organized on file system. User should
    # not have to edit source code
    independent_vw_fnames = [
        'attachment_full_history_vw.sql',
        'chat_full_history_vw.sql',
        'chat_handle_join_full_history_vw.sql',
        'chat_message_join_full_history_vw.sql',
        'contact_names_vw.sql',
        'handle_full_history_vw.sql',
        'message_attachment_join_full_history_vw.sql',
        'message_full_history_vw.sql',
    ]

    # Views that rely on one or more independent view(s)
    dependent_vw_fnames_ordered = [
        'contact_names_vw.sql',
        'message_vw.sql',
        'contact_token_usage_vw.sql',
    ]

    # Dependent views that can be defined in any order
    dependent_vw_fnames_rest = []
    for x in vw_sql_fpaths:
        if basename(x) not in independent_vw_fnames + dependent_vw_fnames_ordered:
            dependent_vw_fnames_rest.append(basename(x))

    # Execute view definitions
    for vw_basename in independent_vw_fnames + dependent_vw_fnames_ordered + dependent_vw_fnames_rest:
        vw_fpath = join(vw_sql_dpath, vw_basename)
        vw_name = splitext(vw_basename)[0]
        vw_sql = read_view_sqlfile(vw_fpath)
        if not dry_run:
            execute_view_def(vw_sql, vw_name, safe, verbose)

    if verbose >= 1:
        vb.info('Refreshed database view definitions', tag=tag)
