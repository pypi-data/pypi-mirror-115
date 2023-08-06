from .common import title_border_left, title_border_right, format_text, read_staged_table_schema, StagedTable
from .transform_operations.exif.exif_tables import exif_tables

def db_transform(pg, vb, pg_schema, sample):
    """
    Apply changes to the database once metadata has been refreshed from source.
    """
    vb.info(f'{title_border_left} {format_text("Staged Tables", "title")} {title_border_right}')

    vb.info(f'EXIF tables', arrow='white')
    exif_tables(pg, vb, pg_schema, sample)
