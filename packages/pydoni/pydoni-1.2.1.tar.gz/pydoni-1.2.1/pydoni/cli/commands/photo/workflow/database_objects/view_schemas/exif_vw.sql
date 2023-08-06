drop view if exists {exif_vw_table_schema}.{exif_vw_table_name};
create view {exif_vw_table_schema}.{exif_vw_table_name} as
select *
from (
{join_exif_tables_sql}
) t1
