import click
from os.path import join, dirname
from .db_views.db_views import define_views
from .transform_operations.staged_tables.staged_table_objects import table_contact_aggregated_stats
from .transform_operations.staged_tables.staged_table_objects import table_emoji
from .transform_operations.staged_tables.staged_table_objects import table_message_emoji_map
from .transform_operations.staged_tables.staged_table_objects import table_message_tokens
from .transform_operations.staged_tables.staged_table_objects import table_tokens


def transform(pg, vb, pg_schema_load, pg_schema_live, full_refresh, dry_run):
    """
    Apply custom data transformations and computations on chat.db raw tables loaded
    into Postgres. Since this step is executed after the 'load' step, processes in
    the 'transform' step have access to a fully updated and fully functional database,
    meaning all views and staged tables in the live schema are available to aid
    in transformation.

    All functions executed in `transform()` must return a `result` dictionary object.
    """
    vb.info(f"->->->->->->->->->->->->-> {click.style('Transform', bold=True)} <-<-<-<-<-<-<-<-<-<-<-<-<-")

    transform_result = {}

    # Ensure all user staged tables exist as one or more views may be dependent on them
    # create_user_staged_tables_if_not_exist(dry_run, pg, vb)
    vb.info('Re-creating empty user staged tables...', bold=True)
    table_objects = [
        table_contact_aggregated_stats,
        table_emoji,
        table_message_emoji_map,
        table_message_tokens,
        table_tokens,
    ]
    for tobject in table_objects:
        if not pg.table_exists(tobject.table_schema, tobject.table_name):
            tobject.create(pg, vb, pg_schema_live, dry_run, suppress_step_name=True)
            if 'rowid' in pg.col_names(tobject.table_schema, tobject.table_name):
                pg.execute(f'alter table {tobject.table_schema}.{tobject.table_name} rename column "rowid" to "ROWID"')

    # Re-define all user database views that may depend on user staged tables
    define_views(pg=pg, vb=vb, pg_schema=pg_schema_live, verbose=1, safe=False, dry_run=dry_run)

    #
    # Refresh table: emoji
    #

    table_emoji.wipe(pg, vb, pg_schema_live, dry_run, wipe_because_of_full_refresh=False)
    transform_result['refresh_emoji_text_map'] = table_emoji.refresh(
        pg=pg,
        vb=vb,
        tag=table_emoji.tag,
        dry_run=dry_run,
        table_schema=table_emoji.table_schema,
        table_name=table_emoji.table_name)

    #
    # Refresh table: contact_aggregated_stats
    #

    table_contact_aggregated_stats.wipe(pg, vb, pg_schema_live, dry_run, wipe_because_of_full_refresh=False)
    transform_result['refresh_contact_aggregated_stats'] = table_contact_aggregated_stats.refresh(
        pg=pg,
        vb=vb,
        tag=table_contact_aggregated_stats.tag,
        dry_run=dry_run,
        table_schema=table_contact_aggregated_stats.table_schema,
        table_name=table_contact_aggregated_stats.table_name,
        acceptable_token_languages=['en', 'nl', 'el', 'emoji'])

    #
    # Refresh table: message_emoji_map
    #

    if full_refresh:
        table_message_emoji_map.wipe(pg, vb, pg_schema_live, dry_run, wipe_because_of_full_refresh=True)

    transform_result['refresh_message_emoji_map'] = table_message_emoji_map.refresh(
        pg=pg,
        vb=vb,
        tag=table_message_emoji_map.tag,
        dry_run=dry_run,
        table_schema=pg_schema_live,
        table_name=table_message_emoji_map.table_name,
        emoji_table=table_emoji)

    #
    # Refresh table: message_tokens
    #

    if full_refresh:
        table_message_tokens.wipe(pg, vb, pg_schema_live, dry_run, wipe_because_of_full_refresh=True)

    transform_result['refresh_message_tokens'] = table_message_tokens.refresh(
        pg=pg,
        vb=vb,
        tag=table_message_tokens.tag,
        dry_run=dry_run,
        table_schema=table_message_tokens.table_schema,
        table_name=table_message_tokens.table_name,
        limit=None,
        batch_size=1500,
        message_tokens_table=table_message_tokens
    )

    #
    # Refresh table: tokens
    #

    if full_refresh:
        table_tokens.wipe(pg, vb, pg_schema_live, dry_run, wipe_because_of_full_refresh=True)

    transform_result['refresh_tokens'] = table_tokens.refresh(
        pg=pg,
        vb=vb,
        tag=table_tokens.tag,
        dry_run=dry_run,
        table_schema=table_tokens.table_schema,
        table_name=table_tokens.table_name,
        limit=None,
        message_tokens_table=table_message_tokens
    )

    vb.info('Postgres iMessage data successfully transformed ✔️', bold=True)

    return transform_result
