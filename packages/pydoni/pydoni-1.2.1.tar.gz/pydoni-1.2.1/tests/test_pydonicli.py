"""Test pydoni command-line interface commands"""

import pydoni
import time
import unittest
from click.testing import CliRunner
from os import remove, chdir, stat
from os.path import join, dirname, abspath, isfile, splitext
from pydoni.cli.commands.cli_audio import compress
from pydoni.cli.commands.cli_audio import join_files
from pydoni.cli.commands.cli_audio import text_to_speech
from pydoni.cli.commands.cli_audio import text_to_speech
from pydoni.cli.commands.cli_audio import to_mp3
from pydoni.cli.commands.cli_data import append_backup_log_table
from pydoni.cli.commands.cli_data import backup
from pydoni.cli.commands.cli_data import pg_dump
from pydoni.cli.commands.cli_video import to_gif
from pydoni.cli.commands.imessage.workflow_elt.workflow_elt import workflow_elt
from requests.api import delete


class TestPydoniCLI(unittest.TestCase):
    """
    Tests for `pydoni` CLI.
    """
    def test_audio_compress(self):
        mp3_fpath = join(tests_dir, 'test_data/music/test_us_and_them_short.mp3')

        # Suffix must match suffix set by default in pydoni.Audio.compress source code
        # when `output_fpath` is None
        expected_output_fpath = pydoni.append_filename_suffix(mp3_fpath, '-COMPRESSED')

        if isfile(expected_output_fpath):
            remove(expected_output_fpath)

        args = ['--fpath', mp3_fpath, '--verbose']
        result = runner.invoke(compress, args)

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(isfile(expected_output_fpath))

        if isfile(expected_output_fpath):
            remove(expected_output_fpath)

    def test_audio_join_files(self):
        mp3_fpath1 = join(tests_dir, 'test_data/music/test_us_and_them_short_first_half.m4a')
        mp3_fpath2 = join(tests_dir, 'test_data/music/test_us_and_them_short_second_half.m4a')

        expected_output_fpath = pydoni.append_filename_suffix(mp3_fpath1, '-JOINED')
        if isfile(expected_output_fpath):
            remove(expected_output_fpath)

        args = [
            '--fpath', mp3_fpath1,
            '--fpath', mp3_fpath2,
            '--output-fpath', expected_output_fpath,
            '--verbose'
        ]
        result = runner.invoke(join_files, args)

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(isfile(expected_output_fpath))

        if isfile(expected_output_fpath):
            remove(expected_output_fpath)

    def test_audio_to_mp3(self):
        m4a_fpath = join(tests_dir, 'test_data/music/test_us_and_them_short.m4a')
        mp3_output = splitext(m4a_fpath)[0] + '-CONVERTED.mp3'

        if isfile(mp3_output):
            remove(mp3_output)

        args = ['--fpath', m4a_fpath, '--verbose']
        result = runner.invoke(to_mp3, args)
        if result.exception is not None:
            raise result.exception

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(isfile(mp3_output))

        if isfile(mp3_output):
            remove(mp3_output)

    def test_audio_text_to_speech(self):
        output_fpath1 = join(tests_dir, 'test_data/music/test_text_to_speech.mp3')
        output_fpath2 = join(tests_dir, 'test_data/music/test_file_to_speech.mp3')

        if isfile(output_fpath1):
            remove(output_fpath1)

        if isfile(output_fpath2):
            remove(output_fpath2)

        args = [
            '--input', 'The quick brown fox jumped over the lazy dog',
            '--input', join(tests_dir, 'test_data/txt/nonempty_dir_flat/test_textfile_15.txt'),
            '--output-fpath', output_fpath1,
            '--output-fpath', output_fpath2,
            '--verbose'
        ]
        result = runner.invoke(text_to_speech, args)
        if result.exception is not None:
            raise result.exception

        self.assertEqual(result.exit_code, 0)
        self.assertTrue(isfile(output_fpath1))
        self.assertTrue(isfile(output_fpath2))

        if isfile(output_fpath1):
            remove(output_fpath1)

        if isfile(output_fpath2):
            remove(output_fpath2)

    def test_data_append_backup_log_table(self):
        table_schema = 'pydonicli'
        table_name = 'directory_backup'

        if pg.table_exists(table_schema, table_name):
            # Ensure proper column structure
            actual_columns = pg.col_names(table_schema, table_name)
            expected_columns = [
                'directory_backup_id',
                'source',
                'source_size_bytes',
                'target',
                'target_size_before_bytes',
                'target_size_after_bytes',
                'start_ts',
                'end_ts',
                'is_completed',
                'gen_ts',
                'mod_ts',
            ]
            self.assertEqual(sorted(actual_columns), sorted(expected_columns))

            only_dir_testing_purposes = join(tests_dir, 'test_data/txt')

            args = [
                '--table-schema', table_schema,
                '--table-name', table_name,
                '--source', only_dir_testing_purposes,
                '--source-size-bytes', stat(only_dir_testing_purposes).st_size,
                '--target', only_dir_testing_purposes,
                '--target-size-before-bytes', stat(only_dir_testing_purposes).st_size,
                '--target-size-after-bytes', stat(only_dir_testing_purposes).st_size,
                '--start-ts', time.time() - 45,
                '--end-ts', time.time(),
                '--is-completed', True,
                '--verbose',
            ]

            result = runner.invoke(append_backup_log_table, args)
            if result.exception is not None:
                raise result.exception

            self.assertEqual(result.exit_code, 0)

            # Clear inserted record from table
            backup_ids = pg.read_sql(f"""
            select directory_backup_id
            from {table_schema}.{table_name}
            where source = '{only_dir_testing_purposes}'
              and target = '{only_dir_testing_purposes}'""")

            if len(backup_ids):
                backup_ids = backup_ids.tolist()
                delete_sql = pg.build_delete(schema_name=table_schema,
                                             table_name=table_name,
                                             pkey_name='directory_backup_id',
                                             pkey_value=backup_ids)
                pg.execute(delete_sql)

    def test_data_backup(self):
        source = join(tests_dir, 'test_data/txt/nonempty_dir_subdirs')
        target = join(tests_dir, 'test_data/txt/nonempty_dir_subdirs_copy_missing_files')

        args = [
            '--source', source,
            '--target', target,
            '--update-log-table',
            # '--use-rsync',
            '--verbose',
            '--debug',
            '--dry-run',
        ]

        result = runner.invoke(backup, args)
        if result.exception is not None:
            raise result.exception

        self.assertEqual(result.exit_code, 0)

    def test_data_pg_dump(self):
        pg_dump_dir = join(tests_dir, 'test_data/pg_dump')

        args = [
            '--backup-dir', pg_dump_dir,
            # '--db-name',
            # '--pg-user',
            '--sep', ","
            '--pgdump',
            '--csvdump',
            '--max-dir-size', 5,
            '--dry-run',
            '--verbose',
        ]

        result = runner.invoke(pg_dump, args)
        if result.exception is not None:
            raise result.exception

        self.assertEqual(result.exit_code, 0)

        self.assertEqual(len(pydoni.listfiles(path=pg_dump_dir, recursive=True)), 0)

    def test_video_to_gif(self):
        video_fpath1 = join(tests_dir, 'test_data/video/test_greek_easter_in_quarantine.mp4')
        video_fpath2 = join(tests_dir, 'test_data/video/test_timelapse.m4v')

        expected_gif_fpath1 = splitext(video_fpath1)[0] + '.gif'
        expected_gif_fpath2 = splitext(video_fpath2)[0] + '.gif'

        if isfile(expected_gif_fpath1):
            remove(expected_gif_fpath1)

        if isfile(expected_gif_fpath2):
            remove(expected_gif_fpath2)

        args = [
            '--fpath', video_fpath1,
            '--fpath', video_fpath2,
            '--verbose',
            '--notify',
        ]

        result = runner.invoke(to_gif, args)
        if result.exception is not None:
            raise result.exception

        self.assertEqual(result.exit_code, 0)

        self.assertTrue(isfile(expected_gif_fpath1))
        self.assertTrue(isfile(expected_gif_fpath2))

        if isfile(expected_gif_fpath1):
            remove(expected_gif_fpath1)

        if isfile(expected_gif_fpath2):
            remove(expected_gif_fpath2)

    def test_imessage_workflow_elt(self):
        args = [
            '--verbose',
        ]

        # result = runner.invoke(workflow_elt, args)
        # if result.exception is not None:
        #     raise result.exception

        # self.assertEqual(result.exit_code, 0)


tests_dir = dirname(abspath(__file__))
root_dir = dirname(tests_dir)
chdir(root_dir)

pg = pydoni.Postgres(credentials_fpath='~/.pgpass')
runner = CliRunner()
case = TestPydoniCLI()

test_methods = [x for x in dir(case) if x.startswith('test_')]
for method in test_methods:
    getattr(case, method)()
