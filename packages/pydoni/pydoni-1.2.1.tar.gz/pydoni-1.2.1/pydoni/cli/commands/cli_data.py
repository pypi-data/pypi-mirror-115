import click
import datetime
import pathlib
import pydoni
import shutil
import subprocess
import termtables as tt
import time
from .common import Verbose
from os import makedirs, stat, mkdir, rmdir
from os.path import basename, dirname, isfile, isdir, getmtime, join, getctime, expanduser
from send2trash import send2trash


@click.option('--table-schema', type=str, default='pydonicli',
              help='Postgres directory backup table schema name.')
@click.option('--table-name', type=str, default='directory_backup',
              help='Postgres directory backup table name.')
@click.option('--source', type=str,
              help='Source directory path.')
@click.option('--source-size-bytes', type=int, default=None,
              help='Size of source directory in bytes.')
@click.option('--target', type=str,
              help='Target directory path.')
@click.option('--target-size-before-bytes', default=None, type=int,
              help='Size of target directory before backup in bytes.')
@click.option('--target-size-after-bytes', default=None, type=int,
              help='Size of target directory after backup in bytes.')
@click.option('--start-ts', type=float, default=None,
              help='UNIX timestamp of backup start time (output of `time.time()`).')
@click.option('--end-ts', type=float, default=None,
              help='UNIX timestamp of backup end time (output of `time.time()`).')
@click.option('--is-completed', type=bool, default=True,
              help='Boolean flag to indicate whether backup was completed successfully.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to console.')
@click.command()
def append_backup_log_table(table_schema,
                            table_name,
                            source,
                            source_size_bytes,
                            target,
                            target_size_before_bytes,
                            target_size_after_bytes,
                            start_ts,
                            end_ts,
                            is_completed,
                            verbose):
    """
    Append a record to directory backup Postgres table. To be used if a backup is carried
    out without the use of the `pydoni data backup` command which handles the table insert
    automatically, but when the backup would still like to be logged in the log table.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    vb = Verbose(verbose)
    pg = pydoni.Postgres()

    sql_value_dct = dict(source=source,
                         source_size_bytes=source_size_bytes,
                         target=target,
                         target_size_before_bytes=target_size_before_bytes,
                         target_size_after_bytes=target_size_after_bytes,
                         start_ts=datetime.datetime.fromtimestamp(start_ts),
                         end_ts=datetime.datetime.fromtimestamp(end_ts),
                         is_completed=is_completed)

    vb.info(f'table_schema: {table_schema}')
    vb.info(f'table_name: {table_name}')
    for k, v in sql_value_dct.items():
        vb.info(f'{k}: {v}')

    insert_sql = pg.build_insert(schema_name=table_schema,
                                 table_name=table_name,
                                 columns=[k for k, v in sql_value_dct.items()],
                                 values=[v for k, v in sql_value_dct.items()])

    pg.execute(insert_sql)

    vb.info(f'Appended record to {table_schema}.{table_name}')
    result['sql_value_dct'] = sql_value_dct

    vb.program_complete('Append to backup log table complete')

    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='data.append_backup_log_table'))


def is_file_changed(sourcefile, targetfile):
    """
    Detect whether a target file has been changed from its corresponding source file
    by determining whether the source and target file change datetimes are different
    by more than a threshold value (i.e. 1%).
    """
    def pct_change(num1, num2):
        """
        Return the pecentage change from `num1` -> `num2` on a scale from 0-100.
        """
        return abs(100.0 * (num2*1.0 - num1*1.0) / num1*1.0)

    mtime_source = getmtime(sourcefile)
    mtime_target = getmtime(targetfile)

    return pct_change(mtime_source, mtime_target) > 1.0

@click.option('--source', type=click.Path(exists=True), required=True,
              help='Absolute path to source directory.')
@click.option('--target', type=click.Path(exists=True), required=True,
              help='Absolute path to target directory.')
@click.option('--update-log-table', is_flag=True, default=False,
              help='Add an entry to Postgres table pydonicli.directory_backup')
@click.option('--use-rsync', is_flag=True, default=False,
              help='Use the `rsync` executable instead of python to back up source to target.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')
@click.option('--debug', is_flag=True, default=False,
              help='Print debug messages to console.')
@click.option('--dry-run', is_flag=True, default=False,
              help='Do not execute copy, replace or delete on any files.')
@click.command()
def backup(source, target, update_log_table, use_rsync, verbose, debug, dry_run):
    """
    Back up a source directory to a target directory.

    This function will accept a source and target directories, most often
    on separate external hard drives, and copy all files from the source
    to the target that are either:

        (1) Not in the target directory
        (2) Are in the target directory, but have been updated

    Files in the target that have been deleted in the source will also be deleted.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    start_ts = time.time()
    vb = Verbose(verbose=verbose, debug=debug)
    ws = '  '

    ignore_files = [
        'The Office S09E16 Moving On.mkv',
        'The Office S09E20 Paper Airplanes.mkv',
    ]

    if update_log_table:
        start_ts_utc = datetime.datetime.utcnow()
        pg = pydoni.Postgres()
        directory_backup_table_schema = 'pydonicli'
        directory_backup_table_name = 'directory_backup'

        insert_dict = dict(source=source,
                           source_size_bytes=stat(source).st_size,
                           target=target,
                           target_size_before_bytes=stat(target).st_size,
                           target_size_after_bytes=None,
                           start_ts=start_ts_utc,
                           is_completed=False)

        insert_sql = pg.build_insert(schema_name=directory_backup_table_schema,
                                     table_name=directory_backup_table_name,
                                     columns=list(insert_dict.keys()),
                                     values=list(insert_dict.values()),
                                     validate=True)
        if not dry_run:
            pg.execute(insert_sql)

        directory_backup_id = pg.read_sql(f"""
        select directory_backup_id
        from {directory_backup_table_schema}.{directory_backup_table_name}
        order by gen_ts desc
        limit 1""").squeeze()


    assert source != target, 'Source and target directories must be different'

    if use_rsync:
        cmd_lst = ['rsync', '--delete-before', '-a', '-h', '-u']
        if verbose:
            cmd_lst = cmd_lst + ['-v', '--progress']

        cmd_lst = cmd_lst + [f'"{source}"'] + [f'"{target}"']
        cmd = ' '.join(cmd_lst)

        subprocess.call(cmd, shell=True)

        # progress_flag = ' --progress' if verbose else ''
        # backup_cmd = f'rsync -avhu{progress_flag} --delete-before "{source}" "{target}"'
        # subprocess.call(backup_cmd, shell=True)

    else:
        vb.info(f'Listing files at source: {source}')
        files_source = pydoni.listfiles(path=source, recursive=True, full_names=True)
        vb.debug('Found files at source: ' + str(len(files_source)))
        files_source = [x for x in files_source if x not in ignore_files]
        vb.debug(f'Found files at source after filtering out manually ignored files: {len(files_source)}')

        vb.info(f'Listing files at target: {target}')
        files_target = pydoni.listfiles(path=target, recursive=True, full_names=True)
        vb.debug('Found files at target: ' + str(len(files_target)))
        files_target = [x for x in files_target if x not in ignore_files]
        vb.debug(f'Found files at target after filtering out manually ignored files: {len(files_target)}')

        # Scan source files and for each determine whether to do nothing, copy to target,
        # or replace at target
        copied_files = []
        replaced_files = []
        vb.info('Scanning for new, updated or deleted files at source')
        vb.pbar_init(total=len(files_source), unit='file')

        for sourcefile in files_source:
            vb.pbar_write(f'Sourcefile: {sourcefile}', refer_debug=True)
            vb.pbar.set_postfix({'file': basename(sourcefile)})

            targetfile = sourcefile.replace(source, target)
            vb.pbar_write(f'{ws}Expected mirrored targetfile: {targetfile}', refer_debug=True)

            if not isfile(targetfile):
                # Copy file to target. Create parent directory at target if not exists
                vb.pbar_write(f'{ws}(Copy) attempting to copy file "{sourcefile}" to "{targetfile}"', refer_debug=True)

                targetdpath = dirname(targetfile)
                if not isdir(targetdpath):
                    vb.pbar_write(f'{ws}{ws}Parent directory of targetfile does not exist, creating it at: ' + targetdpath, refer_debug=True)
                    if not dry_run:
                        makedirs(targetdpath)

                    vb.pbar_write(f'{ws}{ws}Successful', refer_debug=True)

                if not dry_run:
                    shutil.copy2(sourcefile, targetfile)

                vb.pbar_write(f'{ws}Successful', refer_debug=True)
                copied_files.append(sourcefile)

            elif isfile(targetfile) and is_file_changed(sourcefile, targetfile):
                # Replace file at target (same action as copy, but parent directory must exist)
                vb.pbar_write(f'(Replace) attempting to copy file "{sourcefile}" to "{targetfile}"', refer_debug=True)
                if not dry_run:
                    shutil.copy2(sourcefile, targetfile)

                vb.pbar_write(f'Successful', refer_debug=True)
                replaced_files.append(sourcefile)

            else:
                vb.pbar_write(f'{ws}Targetfile already exists and is unchanged', refer_debug=True)

            vb.pbar_update(1)

        vb.pbar_close()

        # Scam target files and for each determine whether that file has been since
        # deleted from source
        deleted_files = []
        vb.info('Scanning for files at target since deleted from source')
        vb.pbar_init(total=len(files_target))
        for targetfile in files_target:
            sourcefile = targetfile.replace(target, source)
            vb.pbar.set_postfix({'file': basename(targetfile)})

            if not isfile(sourcefile) and not isdir(sourcefile):
                vb.pbar_write(f'(Delete) attempting to delete "{targetfile}"', refer_debug=True)
                if not dry_run:
                    send2trash(targetfile)

                vb.pbar_write(f'{ws}Successful', refer_debug=True)
                deleted_files.append(targetfile)

            vb.pbar_update(1)

        vb.pbar_close()

        # Record number of files copied, replaced and deleted
        vb.info(f'Copied {len(copied_files)} files')
        vb.info(f'Replaced {len(replaced_files)} files')
        vb.info(f'Deleted {len(deleted_files)} files')
        vb.info(f'Unchanged {len(files_source) - len(copied_files) - len(replaced_files) - len(deleted_files)} files')
        result = dict(copied=len(copied_files),
                      replaced=len(replaced_files),
                      deleted=len(deleted_files),
                      unchanged=len(files_source) - len(copied_files) - len(replaced_files) - len(deleted_files))

    if update_log_table:
        vb.debug('Attempting to update log table with results...')

        update_dict = dict(target_size_after_bytes=pydoni.dirsize(target),
                           end_ts=datetime.datetime.utcnow(),
                           is_completed=True)

        update_sql = pg.build_update(schema_name=directory_backup_table_schema,
                                     table_name=directory_backup_table_name,
                                     pkey_name='directory_backup_id',
                                     pkey_value=directory_backup_id,
                                     columns=list(update_dict.keys()),
                                     values=list(update_dict.values()),
                                     validate=True)

        if not dry_run:
            pg.execute(update_sql)

        vb.debug(f'{ws}Successful')

    vb.program_complete('Backup complete', start_ts=start_ts)
    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='data.backup'))


@click.option('--backup-dir', type=click.Path(exists=True), required=True,
              help='Path to directory to save database dump to.')
@click.option('--db-name', type=str, default=None,
              help='Name of local Postgres database to dump.')
@click.option('--pg-user', type=str, default=None,
              help='Username for Postgres.')
@click.option('--sep', type=str, default='\x08',
              help='Separator for local CSV dump. Requires that `csvdump` is True.')
@click.option('--pgdump', is_flag=True, default=True,
              help='Dump database using `pgdump` utility.')
@click.option('--csvdump', is_flag=True, default=False,
              help='Dump database as CSV files.')
@click.option('--max-dir-size', type=float, default=None, required=False,
              help=pydoni.advanced_strip("""Maximum backup directory size in GB. If
              specified, after the dump is complete, check if the total directory
              size of `backup_dir` is above this limit. If so, begin by removing the
              oldest backups and re-checking until the size is under the specified
              GB limit."""))
@click.option('--dry-run', is_flag=True, default=False,
              help='Do not execute dump but still run through program.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')
@click.command()
def pg_dump(backup_dir,
            db_name,
            pg_user,
            sep,
            pgdump,
            csvdump,
            max_dir_size,
            dry_run,
            verbose):
    """
    Dump a local Postgres database. Looks for ~/.pgpass by default.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    vb = Verbose(verbose)

    if dry_run:
        vb.info('Not executing any code (dry run)')

    # Either `pgdump` or `csvdump` must be true
    assert pgdump is True or csvdump is True

    if pg_user is not None and db_name is not None:
        pg = pydoni.Postgres(pg_user=pg_user, db_name=db_name)
    else:
        # Attempt to parse ~/.pgpass file. Fail if this file does not exist or is not
        # able to be parsed
        pg = pydoni.Postgres()

    # Define subfolder to dump files to within dump directory
    subdir = pydoni.systime(compact=True) + '_' + pg.db_name
    backup_subdir = join(expanduser(backup_dir), subdir)
    mkdir(backup_subdir)

    vb.info('Database: ' + pg.db_name)
    vb.info('Destination folder: ' + backup_subdir)

    # Dump database based on user's preference
    # May dump using pg_dump, export tables to CSV, or both

    dumped_files = []

    if pgdump:
        vb.info('Executing `pg_dump`')
        if not dry_run:
            dumped_dbfile = pg.dump(backup_dir=backup_subdir)
            dumped_files += [dumped_dbfile]

    if csvdump:
        # Dump each file to textfile
        vb.info('Executing CSV dump to tables')
        if not dry_run:
            dumped_csvfiles = pg.dump_tables(backup_dir=backup_subdir, sep=sep, coerce_csv=False)
            dumped_files += dumped_csvfiles

    result['backup_directory'] = backup_subdir
    result['dumped_files'] = {}
    for f in dumped_files:
        result['dumped_files'][basename(f)] = dict(
            filesize=stat(f).st_size,
            filesize_readable=pydoni.human_filesize(stat(f).st_size),
            created=datetime.datetime.fromtimestamp(getctime(f)).strftime('%Y-%m-%d %H:%M:%S.%f'),
            rows=pydoni.textfile_len(f))

    if verbose:
        vb.line_break()
        tt_list = [[basename(file),
                    infodict['created'],
                    pydoni.human_filesize(infodict['filesize']),
                    str(infodict['rows'])
                   ] for file, infodict in result['dumped_files'].items()]

        if len(tt_list):
            if verbose:
                print(tt.to_string(
                    tt_list,
                    header=[click.style(x, bold=True) for x in ['File', 'Created', 'Size', 'Rows']],
                    style=tt.styles.ascii_thin_double,
                    padding=(0, 1),
                    alignment='ccrr'))
        else:
            vb.warn('No database files were dumped!')

    if dry_run:
        rmdir(backup_subdir)

    max_dir_size_enforced = False
    removed_old_backup_dirs = []
    if max_dir_size:
        # Check size of `backup_dir` and clear any backup directories until the total size
        # is less than max_dir_size (upper GB limit)
        subdirs = sorted([x for x in pathlib.Path(backup_dir).iterdir() if isdir(x)], key=getmtime)
        subdirs_size = zip(subdirs, [pydoni.dirsize(x) / 1e9 for x in subdirs])
        total_size = sum([y for x, y in subdirs_size])

        if total_size > max_dir_size:
            vb.warn(f'Enforcing maximum directory size: {str(max_dir_size)} GB')
            max_dir_size_enforced = True

        while total_size > max_dir_size:
            dir_to_remove = str(subdirs[0])
            shutil.rmtree(dir_to_remove)
            removed_old_backup_dirs.append(dir_to_remove)

            subdirs = sorted([x for x in pathlib.Path(backup_dir).iterdir() if isdir(x)], key=getmtime)

            subdirs_size = zip(subdirs, [pydoni.dirsize(x) / 1e9 for x in subdirs])
            total_size = sum([y for x, y in subdirs_size])

            vb.warn(f'Removed "{basename(dir_to_remove)}"')

    vb.program_complete('Postgres dump complete')

    result['max_dir_size_enforced'] = max_dir_size_enforced
    result['removed_old_backup_dirs'] = [basename(x) for x in removed_old_backup_dirs]

    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='data.pg_dump'))


@click.group(name='data')
def cli_data():
    """Doni data-based CLI tools."""
    pass


cli_data.add_command(backup)
cli_data.add_command(pg_dump)
cli_data.add_command(append_backup_log_table)
