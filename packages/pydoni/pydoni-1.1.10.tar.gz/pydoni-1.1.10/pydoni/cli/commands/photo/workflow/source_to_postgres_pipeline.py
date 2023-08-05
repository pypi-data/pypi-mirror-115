import ast
import click
import datetime
import pandas as pd
import pydoni
from .common import title_border_left, title_border_right, format_text, read_staged_table_schema, define_view
from os.path import splitext, getsize, getmtime, join, dirname, isdir
from pydoni import EXIF


filebase_columns = ['fpath', 'ftype', 'fsize', 'fmod_ts', 'logged_ts',]


def build_filebase_dataframe(fpaths):
    """
    Read base metadata as a dataframe from a list of absolute filepaths.
    """
    ext_map = {
        '.jpg': 'photo',
        '.jpeg': 'photo',
        '.dng': 'photo',
        '.arw': 'photo',
        '.cr2': 'photo',
        '.mov': 'video',
        '.mp4': 'video',
        '.mts': 'video',
        '.m4v': 'video',
        '.avi': 'video',
    }

    filebase = pd.DataFrame(columns=[])

    filetypes = []
    filesizes = []
    mtimes = []

    for fpath in fpaths:
        try:
            filetypes.append(ext_map[splitext(fpath)[1].lower()])
        except KeyError:
            filetypes.append('other')

        filesizes.append(getsize(fpath))
        mtimes.append(datetime.datetime.utcfromtimestamp(getmtime(fpath)))

    filebase['fpath'] = fpaths
    filebase['ftype'] = filetypes
    filebase['fsize'] = filesizes
    filebase['fmod_ts'] = mtimes
    filebase['logged_ts'] = datetime.datetime.utcnow()

    return filebase


def list_files_to_scan_for_exif(filebase, filebase_changes, full_rebuild):
    """
    Filter files for only those of type 'photo' or 'video'.
    """
    if full_rebuild:
        fpaths_scan_for_exif = (
            filebase
            .loc[filebase['ftype'].isin(['photo', 'video'])]['fpath']
            .unique()
            .tolist()
        )
    else:
        fpaths_scan_for_exif = (
            filebase_changes
            .loc[filebase_changes['status'].isin(['modified', 'untracked'])]
            ['fpath']
            .tolist()
        )

    return fpaths_scan_for_exif


def extract_exif_metadata_from_files(fpaths):
    """
    Extract EXIF metadata as a melted dataframe with columns 'fpath', 'raw_exif_attr'
    and 'raw_value' given a list of files.
    """
    if len(fpaths):
        exif_dict = EXIF(fpaths).extract()

        df_lst = []
        for fpath, exifd in exif_dict.items():
            # Begin with copy of dictionary
            new_dict = exifd

            # Convert all extracted values to string format. This helps account for lists
            # which will be cleaned up later by literal evaluation
            new_dict = {k: str(v) for k, v in new_dict.items() if k != 'fpath'}

            # Convert to dictionary
            tmpdf = pd.DataFrame(new_dict, index=[0]).T
            tmpdf['fpath'] = fpath

            df_lst.append(tmpdf)
            del tmpdf

        raw_exif = (
            pd.concat(df_lst)
            .reset_index()
            .rename(columns={'index': 'raw_exif_attr', 0: 'raw_value'})
            [['fpath', 'raw_exif_attr', 'raw_value']]
        )

    else:
        raw_exif = pd.DataFrame(columns=['fpath', 'raw_exif_attr', 'raw_value'])

    return raw_exif


def get_filebase_changes(pg, filebase, pg_schema, filebase_table_name):
    """
    Given the most recent filebase queried from source datafiles, logically determine
    for each file whether it has been modified at source, untracked at source, or removed
    from source.
    """

    def get_modified(filebase):
        """
        Given `filebase` (ground truth) and `filebase_history` existing table in the database,
        filter for only files which have a file modification timestamp later at source
        than what is reflected in the database.
        """
        filebase_history = pg.read_table(pg_schema, filebase_table_name)

        # Join the two datasets
        df = filebase.merge(filebase_history, on='fpath')
        df.columns = [x.replace('_x', '_fsys').replace('_y', '_db') for x in df.columns]

        # Apply filter
        df = df.query('fmod_ts_fsys > fmod_ts_db')

        # Keep ground truth column values
        df = df[['fpath'] + [x for x in df.columns if 'fsys' in x]]
        df.columns = [x.replace('_fsys', '') for x in df.columns]

        return df[filebase_columns]


    def get_untracked(filebase):
        """
        Get files that are new at source and are untracked in the database.
        """
        filebase_history = pg.read_table(pg_schema, filebase_table_name)
        df = filebase[~filebase['fpath'].isin(filebase_history['fpath'].unique())]
        return df[filebase_columns]


    def get_removed(filebase):
        """
        List files that have been removed at source
        """
        filebase_history = pg.read_table(pg_schema, filebase_table_name)
        df = filebase_history[~filebase_history['fpath'].isin(filebase['fpath'].unique())]
        return df[filebase_columns]


    modified = get_modified(filebase)
    modified['status'] = 'modified'
    untracked = get_untracked(filebase)
    untracked['status'] = 'untracked'
    removed = get_removed(filebase)
    removed['status'] = 'removed'

    return pd.concat([modified, untracked, removed], axis=0)


def refresh_filebase_history(pg, vb, filebase, pg_schema, table_name, full_rebuild):
    """
    Load the extracted filebase into the Postgres database.
    """
    columnspec = read_staged_table_schema(table_name)
    pg.create_table_if_not_exists(pg_schema, table_name, columnspec)

    if full_rebuild:
        pg.drop_table_if_exists(pg_schema, table_name)
        filebase.to_sql(table_name, pg.dbcon, schema=pg_schema, if_exists='append', index=False)
        vb.info(f'Added {len(filebase)} records', indent=2)

    # Add records for modified or untracked files to the history table
    filebase_changes = get_filebase_changes(pg, filebase, pg_schema, table_name)
    to_append = filebase_changes.loc[filebase_changes['status'].isin(['modified', 'untracked'])].drop('status', axis=1)
    to_append.to_sql(table_name, pg.dbcon, schema=pg_schema, if_exists='append', index=False)
    plural = '' if len(to_append) == 1 else 's'
    vb.info(f'Appended historical records for {len(to_append)} existing file{plural} modified at source', indent=2)

    # Remove deleted file records from history table
    to_remove = filebase_changes.loc[filebase_changes['status'] == 'removed']
    removed_fpaths = to_remove['fpath'].tolist()
    if len(removed_fpaths):
        deleted_fpaths_str = ', '.join(["'" + x + "'" for x in removed_fpaths])
        delete_sql = f"delete from {pg_schema}.{table_name} where fpath in ({deleted_fpaths_str})"
        pg.execute(delete_sql)

    plural = '' if len(to_remove) == 1 else 's'
    vb.info(f'Removed historical records for {len(to_remove)} file{plural} removed from source', indent=2)

    return filebase_changes


def load_exif_history_table(pg, vb, filebase, filebase_changes, pg_schema, table_name, full_rebuild):
    """
    Query EXIF and refresh physicalized table.
    """
    columnspec = read_staged_table_schema(table_name)

    if full_rebuild:
        pg.drop_table_if_exists(pg_schema, table_name)

    pg.create_table_if_not_exists(pg_schema, table_name, columnspec)

    # Extract EXIF metadata from files
    fpaths_scan_for_exif = list_files_to_scan_for_exif(filebase, filebase_changes, full_rebuild)
    vb.info(f'Scanning {len(fpaths_scan_for_exif)} photo/video files for EXIF metadata...', indent=2)
    raw_exif = extract_exif_metadata_from_files(fpaths_scan_for_exif)

    # Append new EXIF records to table
    raw_exif.to_sql(table_name, pg.dbcon, schema=pg_schema, if_exists='append', index=False)
    vb.info(f'Appended {len(raw_exif)} new records across {len(raw_exif["fpath"].unique())} new files', indent=2)


def source_to_postgres_pipeline(pg, vb, source_dpath, pg_schema, sample, full_rebuild):
    """
    Query source mediafiles for metadata.
    """
    vb.info(f'{title_border_left} {format_text("Source to Postgres Pipeline", "title")} {title_border_right}')

    assert isdir(source_dpath), f'Source directory "{source_dpath}" not found!'

    if full_rebuild:
        vb.info(format_text('Prepare database', 'title'))
        pg.drop_and_recreate_schema(pg_schema)
        vb.info(f'Dropped and cre-created schema {format_text(pg_schema, "code")}', arrow='white')

    vb.info(format_text('Load source files into stack', 'title'))
    vb.info(f'Listing source media files at {format_text(source_dpath, "path")}...', arrow='white')
    fpaths = pydoni.listfiles(source_dpath, recursive=True, full_names=True)

    if isinstance(sample, int):
        # Limit to specified number of files in commandline argument `sample`
        if sample > 0:
            import random
            fpaths = random.sample(fpaths, sample)
            vb.warn(f'Artificially limited source to {sample} files', indent=2)

    vb.info(f'{len(fpaths)} source media files found', indent=2)

    vb.info('Gathering source file type, size and modification time...', arrow='white')
    filebase = build_filebase_dataframe(fpaths)
    vb.info(f'Successfully built filebase, shape: {filebase.shape}', indent=2)

    gerund = 'Rebuilding' if full_rebuild else 'Refreshing'

    filebase_table_name = 'filebase_history'
    vb.info(f'{gerund} {format_text(pg_schema + "." + filebase_table_name, "code")}', arrow='white')

    refresh_filebase_history_args = dict(
        pg=pg,
        vb=vb,
        filebase=filebase,
        pg_schema=pg_schema,
        table_name=filebase_table_name,
        full_rebuild=full_rebuild
    )
    filebase_changes = refresh_filebase_history(pg, vb, filebase, pg_schema, filebase_table_name, full_rebuild)

    vb.info(format_text('Extract and load EXIF metadata', 'title'))

    raw_exif_table_name = 'raw_exif_history'
    vb.info(f'{gerund} {format_text(pg_schema + "." + raw_exif_table_name, "code")}', arrow='white')

    load_exif_history_table_args = dict(
        pg=pg,
        vb=vb,
        filebase=filebase,
        filebase_changes=filebase_changes,
        pg_schema=pg_schema,
        table_name=raw_exif_table_name,
        full_rebuild=full_rebuild
    )
    load_exif_history_table(**load_exif_history_table_args)

    vb.info(format_text('Define database objects', 'title'))
    vb.info('Defining views...', arrow='white')
    define_view(pg, 'filebase_vw')
    vb.info(f'{format_text("filebase_vw", "code")}', indent=2)


    vb.info(format_text('Postgres database successfuully refreshed with source file metadata ✔️', 'title'))
