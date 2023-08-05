import sys, os
sys.path.append(os.path.dirname(__file__))

import numpy as np
import exif_cleaning as ec
import json
import pandas as pd
from ...common import StagedTable, define_view, find_view, format_text
from os.path import join, dirname, isfile


def long_to_wide(df, *args, **kwargs):
    """
    Cast a long dataframe to wide format.
    """
    df = df.pivot(*args, **kwargs)
    df = df.replace('nan', np.NaN)
    df.columns.name = None
    return df


def clean_wide_exif(raw_exif_wide, column_exif):
    """
    Apply the cleaning instructions specified in `column_exif` on the
    dataframe `raw_exif_wide`. Cleaning involves modifying dataframe
    column names as well as ensuring every value in each column conforms
    to the specified datatype.
    """
    cleaned_exif_wide = pd.DataFrame()

    for col_name, col_data in column_exif.items():
        if col_name not in raw_exif_wide.columns:
            continue

        # Set column with `short_name` in target dataframe
        col_short_name = col_data['short_name']
        cleaned_exif_wide[col_short_name] = raw_exif_wide[col_name]

        # Apply cleaning measures if specified
        for idx, clean_process_dct in col_data['cleaning_process_ordered'].items():
            clean_func_name = 'ec.' + clean_process_dct['function_name']
            clean_func_obj = eval(clean_func_name)

            def clean_func_w_args(x):
                return clean_func_obj(x, **clean_process_dct['args'])

            try:
                # Attempt to apply cleaning function on column data
                cleaned_exif_wide[col_short_name] = cleaned_exif_wide[col_short_name].apply(clean_func_w_args)

            except:
                # Find the problem value
                cleaned_items = []
                for item in cleaned_exif_wide[col_short_name]:
                    try:
                        cleaned_items.append(clean_func_w_args(item))
                    except Exception as e:
                        vb.info(f"Couldn't apply function '{clean_process_dct['function_name']}' on value '{str(item)}' (dtype: {type(item)}) in column '{col_name}'")
                        raise e

        # Validate datatype of column
        expected_dtype = col_data['sql_dtype']
        if expected_dtype == 'bool':
            # Pandas will not automatically coerce a True/False/None column to bool, so explicitly cast it here
            # before validating that column's datatype
            try:
                cleaned_exif_wide[col_short_name] = cleaned_exif_wide[col_short_name].astype(bool)
            except Exception as e:
                vb.info(f"Unable to coerce column '{col_name}' to boolean!")
                vb.info('Here is the `.value_counts()` output of the series:')
                vb.info(str(cleaned_exif_wide[col_short_name].value_counts()))
                raise Exception(e)

        cleaned_col_dtype = str(cleaned_exif_wide[col_short_name].dtype)
        error_msg = "Cleaned column '{col_short_name}' is expected as type '{expected_dtype}' but is actually type '{cleaned_col_dtype}'"

        if expected_dtype == 'float':
            if 'float' not in cleaned_col_dtype:
                raise Exception(error_msg.format(**locals()))
        elif expected_dtype == 'int':
            if 'int' not in cleaned_col_dtype:
                raise Exception(error_msg.format(**locals()))
        elif expected_dtype == 'bool':
            if cleaned_col_dtype != 'bool':
                raise Exception(error_msg.format(**locals()))
        elif expected_dtype == 'varchar':
            # All datatypes acceptable for varchar columns
            pass

    return cleaned_exif_wide.fillna(np.NaN)


def recreate_individual_exif_tables(pg, vb, column_exif, pg_schema, cleaned_exif_wide):
    """
    Recreate each individual EXIF table, one for each group specified
    in `column_exif`.
    """
    exif_column_groups = {}
    for col_name, col_data in column_exif.items():
        group_name = col_data['group']
        cleaned_col_name = col_data['short_name']

        if group_name not in exif_column_groups.keys():
            exif_column_groups[group_name] = []

        exif_column_groups[group_name].append(cleaned_col_name)

    # Drop exif_vw if it exists (will be re-created later)
    pg.drop_view_if_exists(pg_schema, 'exif_vw')

    # Each exif group gets its own table keyed on `fpath`
    for group_name, group_col_lst in exif_column_groups.items():
        group_col_lst = [x for x in group_col_lst if x in cleaned_exif_wide.columns]
        exif_subset = EXIFSubset(group_name, group_col_lst, cleaned_exif_wide)
        exif_subset.df.to_sql(exif_subset.table_name, pg.dbcon, schema=pg_schema, if_exists='replace', index=False)
        vb.info(f'{format_text(pg_schema + "." + exif_subset.table_name, "code")}', indent=3)


class EXIFSubset(object):
    """
    Store data for a column-wise subset of the cleaned, wide-format
    EXIF dataframe.
    """
    def __init__(self, group_name, column_lst, cleaned_exif_wide):
        self.group_name = group_name
        self.column_lst = column_lst
        self.table_name = 'exif_' + group_name
        self.df = cleaned_exif_wide[column_lst].reset_index().copy()

    def build_select_sql(self, pg_schema, pkey):
        """
        Build SQL to select from this table in SQL in format:

        select col1, col2, ...
        from pg_schema.table_name
        """
        column_lst = [pkey] + self.column_lst
        column_str = ', '.join(column_lst)
        sql = f"select {column_str}\nfrom{pg_schema}.{self.table_name}"
        return sql


def define_exif_vw(pg, template_fpath, pg_schema, table_name, pkey):
    """
    Maintain view that joins all EXIF tables on a primary key.
    """
    def build_exif_vw_sql(pg, pg_schema, table_name, pkey):
        """
        Build the SQL used to create `exif_vw`.
        """

        exif_vw_table_schema = pg_schema
        exif_vw_table_name = table_name

        exif_tables = pg.list_tables(pg_schema)
        exif_tables = exif_tables.loc[exif_tables['table_name'].str.startswith('exif')]

        ws = '    '
        pkey = 'fpath'

        join_template_str = """
        join {pg_schema}.{table_name}
          {ws}on {base_table_schema}.{base_table_name}.{pkey} = {pg_schema}.{table_name}.{pkey}
        """.strip()

        # Pick an arbitrary table to serve as the 'base' table to join all other
        # exif* tables onto. All exif* tables have the exact same index, so it does
        # not matter which is chosen
        base_table_schema = exif_tables.iloc[0]['table_schema']
        base_table_name = exif_tables.iloc[0]['table_name']

        columns = [base_table_schema + '.' + base_table_name + '.' + pkey]

        join_exif_tables_sql_lst = [
            'select {columns}',
            'from {base_table_schema}.{base_table_name}',
        ]

        for i, row in exif_tables.iterrows():
            pg_schema = row['table_schema']
            table_name = row['table_name']

            column_lst = pg.col_names(pg_schema, table_name)
            column_lst = [pg_schema + '.' + table_name + '.' + x for x in column_lst if x != pkey]
            columns += column_lst

            if table_name != base_table_name:
                join_exif_tables_sql_lst.append(join_template_str.format(**locals()))


        columns = '\n' + ',\n'.join([ws*2 + x for x in columns])

        join_exif_tables_sql_lst_fmt = []
        for x in join_exif_tables_sql_lst:
            join_exif_tables_sql_lst_fmt.append(x.format(**locals()))

        join_exif_tables_sql = '\n'.join([ws + x for x in join_exif_tables_sql_lst_fmt])

        exif_vw_sql = exif_vw_template.format(**locals())
        return exif_vw_sql


    with open(template_fpath, 'r') as f:
        exif_vw_template = f.read()

    exif_vw_sql = build_exif_vw_sql(pg=pg,
                                    pg_schema=pg_schema,
                                    table_name=table_name,
                                    pkey=pkey)
    pg.execute(exif_vw_sql)


def exif_tables(pg, vb, pg_schema, sample):
    """
    Build and maintain staged EXIF tables and view.
    """
    if sample:
        import random
        vb.warn(f'Reading raw EXIF history database table limited to {sample} random source files...', indent=2)
        fpaths = pg.read_sql('select distinct fpath from photo.filebase_vw').squeeze().tolist()
        fpaths = random.sample(fpaths, sample)
        fpaths_str = ', '.join(["'" + x.replace("'", "''") + "'" for x in fpaths])
        raw_exif_long = pg.read_sql(f"""
        select *
        from {pg_schema}.raw_exif_history
        where fpath in ({fpaths_str})
        """)
    else:
        vb.info('Reading raw EXIF history database table...', indent=2)
        raw_exif_long = pg.read_table('photo', 'raw_exif_history')

    column_exif_json_fpath = join(dirname(__file__), 'column_exif.json')
    with open(column_exif_json_fpath) as f:
        column_exif = json.loads(f.read())
        exif_attrs_lst = list(column_exif.keys())

    vb.info('Casting EXIF data from long to wide format...', indent=2)
    raw_exif_latest_per_file = raw_exif_long.loc[raw_exif_long.groupby('fpath')['logged_ts'].idxmax()]
    raw_exif_latest_per_file_filtered = raw_exif_latest_per_file.loc[raw_exif_long['raw_exif_attr'].isin(exif_attrs_lst)]
    raw_exif_latest_per_file_filtered_wide = long_to_wide(raw_exif_latest_per_file_filtered, index='fpath', columns='raw_exif_attr', values='raw_value')

    vb.info('Cleaning wide EXIF data...', indent=2)
    cleaned_exif_wide = clean_wide_exif(raw_exif_latest_per_file_filtered_wide, column_exif)

    vb.info('Re-creating individual EXIF tables...', indent=2)
    recreate_individual_exif_tables(pg, vb, column_exif, pg_schema, cleaned_exif_wide)

    define_exif_vw(pg=pg,
                   template_fpath=find_view('exif_vw'),
                   pg_schema=pg_schema,
                   table_name='exif_vw',
                   pkey='fpath')

    vb.info(f'Re-defined {format_text("exif_vw", "code")}', indent=2)
