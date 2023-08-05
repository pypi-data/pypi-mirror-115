from ...elt_logging.elt_logging import ColorTag
from .refresh_functions.emoji_text_map import refresh_emoji_text_map
from .refresh_functions.contact_aggregated_stats import refresh_contact_aggregated_stats
from .refresh_functions.message_emoji_map import refresh_message_emoji_map
from .refresh_functions.message_tokens import refresh_message_tokens
from .refresh_functions.tokens import refresh_tokens


class StagedTable(object):
    """
    Regularize information stored for all user staged tables.
    """
    def __init__(self, table_schema, table_name, columnspec, refresh_function):
        self.table_schema = table_schema
        self.table_name = table_name
        self.step_name = table_name.replace('_', '-')
        self.tag = ColorTag()
        self.tag.add(self.step_name)
        self.columnspec = columnspec
        self.columns = [x for x, y in self.columnspec]
        self.refresh_function = refresh_function

    def wipe(self, pg, vb, pg_schema_live, dry_run, wipe_because_of_full_refresh):
        """
        Delete all rows from an existing table if workflow is not being run in
        dry run mode. If table doesn't exist, do not execute any SQL and continue.
        """
        tag = ColorTag()

        if not dry_run:
            pg.wipe_table(pg_schema_live, self.table_name)

        tag.add(self.step_name)
        if wipe_because_of_full_refresh:
            tag.add('full-refresh')

        if dry_run:
            tag.add('dry-run')

        msg = f'Wiped table {pg_schema_live}.{self.table_name}'
        vb.info(msg, tag=tag)

    def create(self, pg, vb, pg_schema_live, dry_run, suppress_step_name=False):
        """
        Create a Postgres table (with no data) given a column specification.
        """
        tag = ColorTag()

        if dry_run:
            tag.add('dry-run')
        else:
            pg.create_table(pg_schema_live, self.table_name, self.columnspec)

        msg = f'Created Postgres table: {pg_schema_live}.{self.table_name}'
        vb.info(msg, arrow='white', tag=tag)

    def create_if_not_exists(self, pg, vb, pg_schema_live, dry_run, suppress_step_name=False):
        """
        Create a Postgres table given a column specification if it doesn't exist and if
        the workflow is not being run in dry run mode.
        """
        tag = ColorTag()

        if not dry_run:
            was_created = pg.create_table_if_not_exists(pg_schema_live, self.table_name, self.columnspec)
        else:
            tag.add('dry-run')
            was_created = False

        if suppress_step_name:
            tag.reset()

        if was_created:
            msg = f'Created Postgres table: {pg_schema_live}.{self.table_name}'
            vb.info(msg, arrow='white', tag=tag)

        return was_created

    def refresh(self, *args, **kwargs):
        """
        Execute custom refresh function for a particular table. Refresh functions are
        stored as python modules and live in relative directory refresh_functions/
        """
        self.refresh_function(*args, **kwargs)


table_emoji = StagedTable(
    table_schema='imessage',
    table_name='emoji_text_map',
    columnspec=[
        ('emoji', 'text'),
        ('plain_text', 'text'),
    ],
    refresh_function=refresh_emoji_text_map
)

table_contact_aggregated_stats = StagedTable(
    table_schema='imessage',
    table_name='contact_aggregated_stats',
    columnspec=[
        ('contact_name', 'text'),
        ('first_message_date', 'date'),
        ('first_message_date_from_me', 'date'),
        ('first_message_date_from_them', 'date'),
        ('last_message_date', 'date'),
        ('last_message_date_from_me', 'date'),
        ('last_message_date_from_them', 'date'),
        ('n_active_days', 'int'),
        ('n_active_days_from_me', 'int'),
        ('n_active_days_from_them', 'int'),
        ('n_words', 'int'),
        ('n_words_from_me', 'int'),
        ('n_words_from_them', 'int'),
        ('n_characters', 'int'),
        ('n_characters_from_me', 'int'),
        ('n_characters_from_them', 'int'),
        ('n_days_from_first_to_last_message_date', 'int'),
        ('n_days_since_last_message', 'int'),
        ('n_days_since_last_reply_from_me', 'int'),
        ('n_days_since_last_reply_from_them', 'int'),
        ('n_messages', 'int'),
        ('n_messages_from_me', 'int'),
        ('n_messages_from_them', 'int'),
        ('n_messages_where_top_emoji_used', 'int'),
        ('n_messages_where_top_token_used', 'int'),
        ('n_top_emoji_uses', 'int'),
        ('n_top_token_uses', 'int'),
        ('pct_active_days', 'float'),
        ('pct_messages_from_me', 'float'),
        ('pct_messages_from_them', 'float'),
        ('top_emoji', 'text'),
        ('top_emoji_text', 'text'),
        ('top_emoji_first_use_date', 'date'),
        ('top_emoji_last_use_date', 'date'),
        ('top_token', 'text'),
        ('top_token_first_use_date', 'date'),
        ('top_token_last_use_date', 'date'),
    ],
    refresh_function=refresh_contact_aggregated_stats
)

table_message_emoji_map = StagedTable(
    table_schema='imessage',
    table_name='message_emoji_map',
    columnspec=[
        ('message_uid', 'int8'),
        ('has_emoji', 'bool'),
    ],
    refresh_function=refresh_message_emoji_map
)

table_message_tokens = StagedTable(
    table_schema='imessage',
    table_name='message_tokens',
    columnspec=[
        ('message_uid', 'int8'),
        ('source', 'varchar'),
        ('ROWID', 'int8'),
        ('token_idx', 'int8'),
        ('token', 'text'),
        ('pos', 'text'),
        ('pos_simple', 'text'),
    ],
    refresh_function=refresh_message_tokens
)

table_tokens = StagedTable(
    table_schema='imessage',
    table_name='tokens',
    columnspec=[
        ('token', 'text primary key not null'),
        ('length', 'int8'),
        ('stem', 'text'),
        ('lemma', 'text'),
        ('language', 'text'),
        ('is_english_stopword', 'bool'),
        ('is_punct', 'bool'),
        ('gen_ts', "timestamp not null default timezone('utc'::text, now())"),
        ('mod_ts', "timestamp not null default timezone('utc'::text, now())"),
    ],
    refresh_function=refresh_tokens
)
