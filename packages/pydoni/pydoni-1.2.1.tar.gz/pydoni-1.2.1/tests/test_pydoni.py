"""Test pydoni module functions and classes stored in the module's __init__.py"""

import click
import datetime
import time
import shutil
import re
import pandas as pd
import pydoni
import unittest
from os import chdir, remove, getpid
from os.path import dirname, join, abspath, expanduser, splitext, isfile, isdir


class TestPydoni(unittest.TestCase):
    """
    Tests for `pydoni` package.
    """
    # Operating and file systems ---------------

    def test_listfiles(self):
        result_nonrecursive = pydoni.listfiles(path=join(root_dir, 'tests', 'test_data', 'txt', 'nonempty_dir_flat'))
        self.assertGreater(len(result_nonrecursive), 0)

        result_nonrecursive_txt = pydoni.listfiles(path=join(root_dir, 'tests', 'test_data', 'txt', 'nonempty_dir_flat'), ext='txt')
        self.assertGreater(len(result_nonrecursive_txt), 0)
        unique_extensions = list(set([splitext(x)[1] for x in result_nonrecursive_txt]))
        self.assertEqual(len(unique_extensions), 1)
        self.assertEqual(unique_extensions[0], '.txt')

        result_recursive = pydoni.listfiles(path=join(root_dir, 'tests', 'test_data', 'txt', 'nonempty_dir_subdirs'), recursive=True)
        self.assertGreater(len(result_recursive), 0)
        self.assertTrue(any(['subdir_1_1_3' in x for x in result_recursive]))

    def test_listdirs(self):
        result_nonrecursive = pydoni.listdirs(path=join(root_dir, 'tests', 'test_data', 'txt', 'nonempty_dir_flat'))
        self.assertEqual(len(result_nonrecursive), 0)

        result_recursive = pydoni.listdirs(path=join(root_dir, 'tests', 'test_data', 'txt', 'nonempty_dir_subdirs'), recursive=True)
        self.assertGreater(len(result_recursive), 0)
        self.assertTrue(any(['subdir_1_1_3' in x for x in result_recursive]))

    def test_ensurelist(self):
        result = pydoni.ensurelist('test')
        self.assertEqual(result, ['test'])

        result = pydoni.ensurelist(['test'])
        self.assertEqual(result, ['test'])

    def test_systime(self):
        now = pydoni.systime(as_string=False)
        self.assertIsInstance(now, datetime.datetime)
        self.assertLessEqual(now, datetime.datetime.now())

        now_str = pydoni.systime(as_string=True)
        self.assertRegex(now_str, r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')

        now_str_compact = pydoni.systime(as_string=True, compact=True)
        self.assertRegex(now_str_compact, r'^\d{8}_\d{6}$')

    def test_sysdate(self):
        now = pydoni.sysdate(as_string=False)
        self.assertIsInstance(now, datetime.datetime)
        self.assertLessEqual(now, datetime.datetime.now())

        now_str = pydoni.sysdate(as_string=True)
        self.assertRegex(now_str, r'^\d{4}-\d{2}-\d{2}$')

        now_str_compact = pydoni.sysdate(as_string=True, compact=True)
        self.assertRegex(now_str_compact, r'^\d{8}$')

    def test_append_filename_suffix(self):
        txt_fpath = expanduser('~/Desktop/test_file.txt')
        expectation = expanduser('~/Desktop/test_file-1.txt')
        # Doesn't actually create or expect a file on Desktop
        self.assertEqual(pydoni.append_filename_suffix(fpath=txt_fpath, suffix='-1'), expectation)

    def test_textfile_len(self):
        txt_fpath = join(tests_dir, 'test_data/txt/nonempty_dir_subdirs/test_textfile_15.txt')
        self.assertEqual(pydoni.textfile_len(fpath=txt_fpath), 10)

    def test_dirsize(self):
        dpath = join(tests_dir, 'test_data/txt/nonempty_dir_subdirs/subdir_1')
        self.assertEqual(pydoni.dirsize(dpath=dpath), 25187)

    def test_macos_notify(self):
        if pydoni.find_binary('terminal-notifier'):
            pydoni.macos_notify(message='Test notification message',
                                title='Pydoni Pytest',
                                subtitle='Test subtitle')

    # Python object operations ---------------

    def test_advanced_strip(self):
        result = pydoni.advanced_strip("""
        test   """)
        self.assertIsInstance(result, str)
        self.assertEqual(result, 'test')

    def test_naturalsort(self):
        result = pydoni.naturalsort(lst=['1item', '10item', '3item', '2item'])
        expectation = ['1item', '2item', '3item', '10item']
        self.assertEqual(result, expectation)

    def test_fmt_seconds(self):
        result = pydoni.fmt_seconds(time_in_sec=91000, units='auto', round_digits=2)
        self.assertEqual(result['units'], 'days')
        self.assertEqual(result['value'], 1.05)

        result = pydoni.fmt_seconds(time_in_sec=91000, units='seconds', round_digits=2)
        self.assertEqual(result['units'], 'seconds')
        self.assertEqual(result['value'], 91000)

        result = pydoni.fmt_seconds(time_in_sec=91000, units='minutes', round_digits=2)
        self.assertEqual(result['units'], 'minutes')
        self.assertEqual(result['value'], 1516.67)

        result = pydoni.fmt_seconds(time_in_sec=91000, units='hours', round_digits=2)
        self.assertEqual(result['units'], 'hours')
        self.assertEqual(result['value'], 25.28)

        result = pydoni.fmt_seconds(time_in_sec=91000, units='days', round_digits=2)
        self.assertEqual(result['units'], 'days')
        self.assertEqual(result['value'], 1.05)

    def test_listmode(self):
        result = pydoni.listmode(lst=['a', 'b', 'a', 'a', 'c', 'd', 'b'])
        self.assertEqual(result, 'a')

    def test_cap_nth_char(self):
        result = pydoni.cap_nth_char(string='string', n=3)
        self.assertEqual(result, 'strIng')

    def test_replace_nth_char(self):
        result = pydoni.replace_nth_char(string='string', n=3, replacement='I')
        self.assertEqual(result, 'strIng')

    def test_insert_nth_char(self):
        result = pydoni.insert_nth_char(string='strng', n=3, char='I')
        self.assertEqual(result, 'strIng')

    def test_human_filesize(self):
        self.assertEqual(pydoni.human_filesize(1e0), '1 B')
        self.assertEqual(pydoni.human_filesize(1e3), '1.0 KB')
        self.assertEqual(pydoni.human_filesize(1e6), '977 KB')
        self.assertEqual(pydoni.human_filesize(1e9), '954 MB')
        self.assertEqual(pydoni.human_filesize(1e12), '931 GB')
        self.assertEqual(pydoni.human_filesize(1e15), '909 TB')
        self.assertEqual(pydoni.human_filesize(1e18), '888 PB')
        self.assertEqual(pydoni.human_filesize(1e21), '867 EB')
        self.assertEqual(pydoni.human_filesize(1e24), '847 ZB')
        self.assertEqual(pydoni.human_filesize(1e27), '827 YB')

    def test_split_at(self):
        result = pydoni.split_at(lst=['a', 'b', 'c'], idx=1)
        self.assertEqual(result, [['a'], ['b', 'c']])

        result = pydoni.split_at(lst=[1, 2, 3, 4, 5, 6], idx=[2, 4])
        self.assertEqual(result, [[1, 2], [3, 4], [5, 6]])

    def test_duplicated(self):
        result = pydoni.duplicated(lst=['a', 'b', 'b', 'c', 'c', 'c'])
        self.assertEqual(result, [False, False, True, False, True, True])

    def test_test_value(self):
        self.assertEqual(pydoni.test_value('True', 'bool'), True)
        self.assertEqual(pydoni.test_value('true', 'bool'), True)
        self.assertEqual(pydoni.test_value('t', 'bool'), True)
        self.assertEqual(pydoni.test_value('yes', 'bool'), True)
        self.assertEqual(pydoni.test_value('y', 'bool'), True)
        self.assertEqual(pydoni.test_value('False', 'bool'), True)
        self.assertEqual(pydoni.test_value('false', 'bool'), True)
        self.assertEqual(pydoni.test_value('f', 'bool'), True)
        self.assertEqual(pydoni.test_value('no', 'bool'), True)
        self.assertEqual(pydoni.test_value('n', 'bool'), True)
        self.assertEqual(pydoni.test_value('false', 'bool', return_coerced_value=True), False)

        self.assertEqual(pydoni.test_value('abc', 'int'), False)
        self.assertEqual(pydoni.test_value('5', 'int'), True)
        self.assertEqual(pydoni.test_value('5.5', 'integer'), False)

        self.assertEqual(pydoni.test_value('abc', 'float'), False)
        self.assertEqual(pydoni.test_value('5', 'float'), False)
        self.assertEqual(pydoni.test_value('5.5', 'float'), True)

        self.assertEqual(pydoni.test_value('2021-05-16', 'date'), True)
        self.assertEqual(pydoni.test_value('2021-05-16  ', 'date'), True)
        self.assertEqual(pydoni.test_value('2021-05-16 11:46:45', 'date'), False)
        self.assertEqual(pydoni.test_value('abc', 'date'), False)
        self.assertEqual(pydoni.test_value('5.5', 'date'), False)

        self.assertEqual(pydoni.test_value('2021-05-16', 'datetime'), False)
        self.assertEqual(pydoni.test_value('2021-05-16 11:46:45', 'datetime'), True)
        self.assertEqual(pydoni.test_value('abc', 'datetime'), False)
        self.assertEqual(pydoni.test_value('5.5', 'datetime'), False)

        self.assertEqual(pydoni.test_value(expanduser('~/Desktop'), 'path'), True)
        self.assertEqual(pydoni.test_value(expanduser('~/Desktop'), 'path exists'), True)

    def test_extract_colorpalette(self):
        result = pydoni.extract_colorpalette('Blues')
        self.assertEqual(result[0:3], ['#f7fbff', '#f6faff', '#f5fafe'])

    def test_rename_dict_keys(self):
        dct = {'a': 1, 'b': 2, 'c': 3}
        result = pydoni.rename_dict_keys(dct=dct, key_dict={'c': 'd'})
        expectation = {'a': 1, 'b': 2, 'd': 3}
        self.assertEqual(result, expectation)

    def test_collapse_df_columns(self):
        testdf = pd.Series([1, 2, 3], index=['a','b','c']).to_frame().T
        testdf.columns = pd.MultiIndex.from_product([['col_group'], testdf.columns])
        result = list(pydoni.collapse_df_columns(testdf).columns)
        expectation = ['col_group_a', 'col_group_b', 'col_group_c']
        self.assertEqual(result, expectation)

    # Verbosity ---------------

    def test_echo(self):
        sub_out_ts = lambda x: re.sub(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', 'YYYY-mm-dd HH:MM:SS', x)

        msg = pydoni.echo(msg='test', indent=0, timestamp=False, level='T', arrow=None, capture_output=True, fg='blue')
        self.assertEqual(click.unstyle(msg), 'test')
        self.assertEqual(msg, '\x1b[34mtest\x1b[0m')

        msg = pydoni.echo(msg='test', indent=0, timestamp=False, level='T', arrow=None, capture_output=True)
        self.assertEqual(click.unstyle(msg), 'test')

        msg = pydoni.echo(msg='test', indent=2, timestamp=False, level='T', arrow=None, capture_output=True)
        self.assertEqual(click.unstyle(msg), '    test')

        msg = pydoni.echo(msg='test', indent=0, timestamp=True, level='T', arrow=None, capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), '[YYYY-mm-dd HH:MM:SS] test')

        msg = pydoni.echo(msg='test', indent=2, timestamp=True, level='T', arrow=None, capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), '[YYYY-mm-dd HH:MM:SS]     test')

        msg = pydoni.echo(msg='test', indent=0, timestamp=True, level='T', arrow='blue', capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), '[YYYY-mm-dd HH:MM:SS] ==> test')

        msg = pydoni.echo(msg='test', indent=1, timestamp=True, level='T', arrow='yellow', capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), '[YYYY-mm-dd HH:MM:SS]   ==> test')

        msg = pydoni.echo(msg='test', indent=0, timestamp=False, level='S', arrow=None, capture_output=True)
        self.assertEqual(click.unstyle(msg), 'SUCCESS: test')

        msg = pydoni.echo(msg='test', indent=1, timestamp=False, level='S', arrow=None, capture_output=True)
        self.assertEqual(click.unstyle(msg), 'SUCCESS:   test')

        msg = pydoni.echo(msg='test', indent=0, timestamp=False, level='S', arrow='white', capture_output=True)
        self.assertEqual(click.unstyle(msg), 'SUCCESS: ==> test')

        msg = pydoni.echo(msg='test', indent=1, timestamp=False, level='S', arrow='green', capture_output=True)
        self.assertEqual(click.unstyle(msg), 'SUCCESS:   ==> test')

        msg = pydoni.echo(msg='test', indent=0, timestamp=True, level='S', arrow=None, capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), '[YYYY-mm-dd HH:MM:SS] SUCCESS: test')

        msg = pydoni.echo(msg='test', indent=0, timestamp=True, level='S', arrow='blue', capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), '[YYYY-mm-dd HH:MM:SS] SUCCESS: ==> test')

        msg = pydoni.echo(msg='test', indent=3, timestamp=True, level='S', arrow='red', capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), '[YYYY-mm-dd HH:MM:SS] SUCCESS:       ==> test')

        msg = pydoni.echo(msg='test', indent=3, timestamp=True, level='F', arrow='red', capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), '[YYYY-mm-dd HH:MM:SS] FATAL:       ==> test')

        msg = pydoni.echo(msg='test', indent=0, timestamp=True, level='F', arrow=None, capture_output=True)
        self.assertEqual(sub_out_ts(msg), '\x1b[31m[YYYY-mm-dd HH:MM:SS] FATAL: \x1b[0mtest\x1b[0m')

        msg = pydoni.echo(msg='test', indent=1, timestamp=False, level='FATAL', arrow='red', capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), 'FATAL:   ==> test')

        msg = pydoni.echo(msg='test', indent=0, timestamp=False, level='D', arrow=None, capture_output=True)
        self.assertEqual(click.unstyle(msg), '[D] test')

        msg = pydoni.echo(msg='test', indent=0, timestamp=True, level='D', arrow=None, capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), '[YYYY-mm-dd HH:MM:SS D] test')

        msg = pydoni.echo(msg='test', indent=1, timestamp=True, level='D', arrow='white', capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), '[YYYY-mm-dd HH:MM:SS D]   ==> test')

        msg = pydoni.echo(msg='test', indent=0, timestamp=True, level='W', arrow=None, capture_output=True)
        self.assertEqual(sub_out_ts(click.unstyle(msg)), '[YYYY-mm-dd HH:MM:SS W] test')
        self.assertEqual(sub_out_ts(msg), '\x1b[33m[YYYY-mm-dd HH:MM:SS W] \x1b[0mtest\x1b[0m')

        msg = pydoni.echo(msg='test', indent=0, timestamp=True, level='E', arrow=None, capture_output=True)
        self.assertEqual(sub_out_ts(msg), '\x1b[31m[YYYY-mm-dd HH:MM:SS E] \x1b[0mtest\x1b[0m')

    def test_Verbose(self):
        start_ts_time = time.time()
        start_ts_datetime = datetime.datetime.now()
        time.sleep(1)

        vb = pydoni.Verbose(verbose=True, debug=False, timestamp=False)
        vb.echo(msg='test string')
        vb.line_break()
        vb.section_header(msg='Test Header')
        vb.section_header(msg='Test Header', time_in_sec=10)
        vb.program_complete(msg='Program complete', emoji_string=':rocket:')
        vb.program_complete(msg='Program complete', emoji_string=':rocket:', start_ts=start_ts_time)
        vb.program_complete(msg='Program complete', emoji_string=':rocket:', start_ts=start_ts_datetime)

    def test_print_apple_ascii_art(self):
        pydoni.print_apple_ascii_art()
        pydoni.print_apple_ascii_art(by_line=True)
        pydoni.print_apple_ascii_art(by_char=True)

    def test_print_columns(self):
        pydoni.print_columns(lst=['a', 'b', 'c', 'd'], ncol=1)
        pydoni.print_columns(lst=['a', 'b', 'c', 'd'], ncol=2)
        pydoni.print_columns(lst=['a', 'b', 'c', 'd'], ncol=3)
        pydoni.print_columns(lst=['a', 'b', 'c', 'd'], ncol=3, delay=.01)

    def test_stabilize_postfix(self):
        result = pydoni.stabilize_postfix(key='test', max_len=20, fillchar='•', side='right')
        self.assertEqual(result, '••••••••••••••••test')
        result = pydoni.stabilize_postfix(key='test', max_len=10, fillchar='•', side='left')
        self.assertEqual(result, 'test••••••')
        result = pydoni.stabilize_postfix(key='test', max_len=3, fillchar='•', side='left')
        self.assertEqual(result, 'tes')

    # Bash command wrappers ---------------

    def test_syscmd(self):
        result_bytes = pydoni.syscmd('uptime')
        self.assertIsInstance(result_bytes, bytes)

        result_str = pydoni.syscmd('uptime', encoding='utf-8')
        self.assertIsInstance(result_str, str)
        self.assertIn('load averages', result_str)

    def test_find_binary(self):
        result = pydoni.find_binary(bin_name='awk')
        self.assertEqual(result, '/usr/bin/awk')

    def test_adobe_dng_converter(self):
        if pydoni.is_adobe_dng_converter_installed():
            test_arw = join(tests_dir, 'test_data/img/test_longhorns.ARW')
            output_fpath = splitext(test_arw)[0] + '.dng'
            pydoni.adobe_dng_converter(fpath=test_arw)
            self.assertTrue(isfile(output_fpath), msg=f'pydoni.adobe_dng_converter() failed on file "{test_arw}"')
            remove(output_fpath)

    def test_stat(self):
        test_txt = join(tests_dir, 'test_data/txt/nonempty_dir_flat/test_textfile_1.txt')
        result = pydoni.stat(test_txt)
        self.assertEqual(result['Size'], '42')
        self.assertEqual(result['FileType'], '')
        self.assertEqual(result['Mode'], '(0644/-rw-r--r--)')
        self.assertEqual(result['Uid'], '(  501/andonisooklaris)')
        self.assertEqual(result['Device'], '1,4')
        self.assertEqual(result['Inode'], '317387722')
        self.assertEqual(result['Links'], '1')

        test_jpg = join(tests_dir, 'test_data/img/test_playlist_cover.jpg')
        result = pydoni.stat(test_jpg)
        self.assertEqual(result['Size'], '280698')
        self.assertEqual(result['FileType'], '')
        self.assertEqual(result['Mode'], '(0644/-rw-r--r--)')
        self.assertEqual(result['Uid'], '(  501/andonisooklaris)')
        self.assertEqual(result['Device'], '1,4')
        self.assertEqual(result['Inode'], '319518080')
        self.assertEqual(result['Links'], '1')

    def test_mid3v2(self):
        if pydoni.find_binary('mid3v2'):
            mp3_fpath = join(tests_dir, 'test_data/music/test_us_and_them.mp3')

            # Get original artist
            artist_before = 'Pink Floyd'

            # Set 'test artist'
            pydoni.mid3v2(mp3_fpath, attr_name='artist', attr_value='test artist')

            # Make sure 'test artist' was set
            artist_after = pydoni.EXIF(mp3_fpath).extract()[mp3_fpath]['Artist']
            self.assertEqual(artist_after, 'test artist')

            # Reset artist to original
            pydoni.mid3v2(mp3_fpath, attr_name='artist', attr_value=artist_before)

            # Make sure original artist was reset
            artist_reset = pydoni.EXIF(mp3_fpath).extract()[mp3_fpath]['Artist']
            self.assertEqual(artist_reset, 'Pink Floyd')

    def test_mp4_to_mp3(self):
        if pydoni.find_binary('ffmpeg'):
            test_mp4 = join(tests_dir, 'test_data/video/test_greek_easter_in_quarantine.mp4')
            expected_mp3 = splitext(test_mp4)[0] + '.mp3'

            pydoni.mp4_to_mp3(fpath=test_mp4, bitrate='192k')
            self.assertTrue(isfile(expected_mp3))

            if isfile(expected_mp3):
                remove(expected_mp3)

    def test_split_video_scenes(self):
        if pydoni.find_binary('scenedetect'):
            test_video = join(tests_dir, 'test_data/video/test_austin_to_sd_subset.m4v')

            tmp_dpath = join(tests_dir, 'test_data/video', 'tmp_scenedetect')
            if isdir(tmp_dpath):
                shutil.rmtree(tmp_dpath)

            result = pydoni.split_video_scenes(fpath=test_video, output_dpath=tmp_dpath)
            self.assertNotIn('Traceback', result.decode('utf-8'))

            split_files = pydoni.listfiles(path=tmp_dpath)
            if isdir(tmp_dpath):
                shutil.rmtree(tmp_dpath)

            self.assertGreater(len(split_files), 0)

    def test_osascript(self):
        if pydoni.find_binary('osascript'):
            applescript = 'log "test from applescript"'
            pydoni.osascript(applescript)

    # Database operations ---------------

    def test_Postgres(self):
        try:
            pg = pydoni.Postgres()
            connected = True
        except:
            connected = False

        if connected:
            # Not all users of this library will have Postgres set up, so only execute
            # tests if Postgres connected successfully.
            #
            # Now perform a series of commands to ensure that Postgres class methods are
            # working as intended.

            # Method: read_sql(). Choose a default table that always exists
            result = pg.read_sql('select * from information_schema.tables limit 1')

            # Method: get_table_name()
            self.assertEqual(pg.get_table_name(schema_name=None, table_name='pg_stat'), 'pg_stat')
            self.assertEqual(pg.get_table_name(schema_name='information_schema', table_name='tables'), 'information_schema.tables')

            # Method: validate_dtype()
            result = pg.validate_dtype(schema_name='information_schema',
                                       table_name='tables',
                                       col='table_catalog',
                                       val='string value')
            self.assertEqual(result, True)
            result = pg.validate_dtype(schema_name='information_schema',
                                       table_name='tables',
                                       col='table_catalog',
                                       val=5)
            self.assertEqual(result, False)

            # Method: infoschema()
            result = sorted(pg.infoschema(infoschema_table='tables').columns)
            result_sql_direct = sorted(pg.read_sql('select * from information_schema.tables limit 1').columns)
            self.assertEqual(result, result_sql_direct)

            # Method: build_update()
            result = pg.build_update(schema_name='pg_catalog',
                                     table_name='pg_stat_database',
                                     pkey_name='datid',
                                     pkey_value=12345,
                                     columns=['tup_returned', 'tup_fetched'],
                                     values=[11111, 22222],
                                     validate=True,
                                     newlines=False)
            expectation = 'UPDATE pg_catalog.pg_stat_database SET "tup_returned"=11111, "tup_fetched"=22222 WHERE "datid" = 12345'
            self.assertEqual(result, expectation)
            result = pg.build_update(schema_name='pg_catalog',
                                     table_name='pg_stat_database',
                                     pkey_name='datid',
                                     pkey_value=12345,
                                     columns=['tup_returned', 'tup_fetched'],
                                     values=[11111, 22222],
                                     validate=False,
                                     newlines=True)
            expectation = 'UPDATE pg_catalog.pg_stat_database\nSET "tup_returned"=11111, \n    "tup_fetched"=22222\nWHERE "datid" = 12345'
            self.assertEqual(result, expectation)

            # Method: build_insert()
            result = pg.build_insert(schema_name='pg_catalog',
                                     table_name='pg_stat_database',
                                     columns=['tup_returned', 'tup_fetched'],
                                     values=[11111, 22222],
                                     validate=True,
                                     newlines=False)
            expectation = 'insert into pg_catalog.pg_stat_database ("tup_returned", "tup_fetched") values (11111, 22222)'
            self.assertEqual(result, expectation)
            result = pg.build_insert(schema_name='pg_catalog',
                                     table_name='pg_stat_database',
                                     columns=['tup_returned', 'tup_fetched'],
                                     values=[11111, 22222],
                                     validate=False,
                                     newlines=True)
            expectation = 'insert into pg_catalog.pg_stat_database ("tup_returned", "tup_fetched")\nvalues (11111, 22222)'
            self.assertEqual(result, expectation)

            # Method: build_delete()
            result = pg.build_delete(schema_name='pg_catalog',
                                     table_name='pg_stat_database',
                                     pkey_name='datid',
                                     pkey_value=12345,
                                     newlines=False)
            expectation = 'delete from pg_catalog.pg_stat_database where datid = 12345'
            self.assertEqual(result, expectation)
            result = pg.build_delete(schema_name='pg_catalog',
                                     table_name='pg_stat_database',
                                     pkey_name='datid',
                                     pkey_value=12345,
                                     newlines=True)
            expectation = 'delete from pg_catalog.pg_stat_database\nwhere datid = 12345'
            self.assertEqual(result, expectation)

            # Method: col_names()
            result = pg.col_names(schema_name='pg_catalog', table_name='pg_stat_database')
            self.assertIn('datid', result)

            # Method: col_dtypes()
            result = pg.col_dtypes(schema_name='pg_catalog', table_name='pg_stat_database')
            self.assertEqual(result['datid'], 'oid')

            # Method: read_table()
            result = pg.read_table(schema_name='pg_catalog', table_name='pg_stat_database')
            self.assertGreater(result.shape[0], 0)
            self.assertGreater(result.shape[1], 0)

            # Method: dump()
            # Just make sure pg_dump is installed
            pydoni.find_binary('pg_dump', abort=True)

            #
            # All create*, drop* and list* methods
            #

            pid = getpid()
            test_schema_name = f'test_pydoni_schema_{pid}'
            test_table_name = f'test_pydoni_table_{pid}'
            test_view_name = f'test_pydoni_view_{pid}'

            pg.create_schema(schema_name=test_schema_name)

            try:
                # If any of the following fail, delete the test schema and raise error
                columnspec = {'col1': 'int', 'col2': 'text'}
                pg.create_table(schema_name=test_schema_name,
                                table_name=test_table_name,
                                columnspec=columnspec,
                                if_not_exists=False)

                result = pg.table_exists(schema_name=test_schema_name, table_name=test_table_name)
                self.assertTrue(result)

                pg.create_table(schema_name=test_schema_name,
                                table_name=test_table_name,
                                columnspec=columnspec,
                                if_not_exists=True)

                insert_fake_data_sql = pg.build_insert(schema_name=test_schema_name,
                                                    table_name=test_table_name,
                                                    columns=[k for k, v in columnspec.items()],
                                                    values=[5, 'test'],
                                                    validate=False,
                                                    newlines=False)

                pg.execute(insert_fake_data_sql)

                pg.create_view(schema_name=test_schema_name,
                            view_name=test_view_name,
                            view_sql=f'select * from {test_schema_name}.{test_table_name}',
                            or_replace=False)

                result = pg.view_exists(schema_name=test_schema_name, view_name=test_view_name)
                self.assertTrue(result)

                pg.create_view(schema_name=test_schema_name,
                            view_name=test_view_name,
                            view_sql=f'select * from {test_schema_name}.{test_table_name}',
                            or_replace=True)

                result = pg.read_table(schema_name=test_schema_name, table_name=test_view_name)
                self.assertEqual(result.to_dict(), {'col1': {0: 5}, 'col2': {0: 'test'}})

                pg.drop_view(schema_name=test_schema_name, view_name=test_view_name)
                pg.drop_table(schema_name=test_schema_name, table_name=test_table_name)
                pg.drop_schema(schema_name=test_schema_name)

            except Exception:
                pg.drop_schema(schema_name=test_schema_name)
                raise Exception

            # Method: _single_quote()
            self.assertEqual(pg._single_quote(5), 5)
            self.assertEqual(pg._single_quote('test'), "'test'")
            self.assertEqual(pg._single_quote("test's"), "'test''s'")

    # Web tools ---------------

    def test_check_network_connection(self):
        pydoni.check_network_connection(abort=False)

    def test_test_url(self):
        if pydoni.check_network_connection():
            expected_true = pydoni.test_url(url='http://www.google.com', quiet=False)
            self.assertTrue(expected_true, 'Test url www.google.com is not returning True')

            expected_false = pydoni.test_url(url='http://www.google2.com', quiet=False)
            self.assertFalse(expected_false, 'Test url www.google2.com is not returning False')

    def test_get_element_by_selector(self):
        if pydoni.check_network_connection():
            url = 'https://mutagen.readthedocs.io/en/latest/man/mid3v2.html'
            element = pydoni.get_element_by_selector(url=url, selector='h1')
            element = element[0]
            element = element.replace('¶', '')
            self.assertEqual(element, 'mid3v2')

    def test_get_element_by_xpath(self):
        if pydoni.check_network_connection():
            url = 'https://mutagen.readthedocs.io/en/latest/man/mid3v2.html'
            element = pydoni.get_element_by_xpath(url=url, xpath='//h1')
            element = element[0]
            self.assertEqual(element.text, 'mid3v2')

    def test_downloadfile(self):
        if pydoni.check_network_connection():
            img_url = 'https://upload.wikimedia.org/wikipedia/commons/3/33/L%27Image_et_le_Pouvoir_-_Buste_cuirass%C3%A9_de_Marc_Aur%C3%A8le_ag%C3%A9_-_3.jpg'
            destfile = join(tests_dir, 'test_data/img/test_downloadfile.jpg')

            if isfile(destfile):
                remove(destfile)

            pydoni.downloadfile(url=img_url, destfile=destfile, method='requests')
            self.assertTrue(isfile(destfile))

            if isfile(destfile):
                remove(destfile)

            pydoni.downloadfile(url=img_url, destfile=destfile, method='curl')
            self.assertTrue(isfile(destfile))

            if isfile(destfile):
                remove(destfile)

    def test_simple_get_and_is_good_response(self):
        if pydoni.check_network_connection():
            url = 'https://en.wikipedia.org/wiki/Marcus_Aurelius'
            resp_content = pydoni.simple_get(url=url)

    # Image operations ---------------

    def test_make_meme(self):
        img_fpath = join(tests_dir, "test_data/img/test_whats_the_scuttlebutt.png")
        expected_img = pydoni.append_filename_suffix(img_fpath, '-MEME')
        pydoni.make_meme(img_fpath=img_fpath,
                         output_fpath=expected_img,
                         msg="What's the scuttlebutt?",
                         msg_color='white',
                         msg_pos='bottom',
                         msg_outline_color='black',
                         msg_outline_width=3,
                         font_path='/System/Library/Fonts/HelveticaNeue.ttc',
                         font_size=200,
                         repel_from_edge=.05)

        if isfile(expected_img):
            remove(expected_img)

    def test_ocr_image(self):
        img_fpath = join(tests_dir, 'test_data/img/test_ocr_image.png')
        text = pydoni.ocr_image(image_fpath=img_fpath, preprocess=None)
        expectation = 'The quick brown fox jumped over the lazy dog\nNow is the time for all good men to come to the aid of their country'
        self.assertEqual(text.strip(), expectation)

    def test_get_blur_value(self):
        img_fpath_sharp = join(tests_dir, 'test_data/img/test_tsoureki.jpg')
        value_sharp = pydoni.get_blur_value(image_fpath=img_fpath_sharp)

        img_fpath_blur = join(tests_dir, 'test_data/img/test_tsoureki_blur.jpg')
        value_blur = pydoni.get_blur_value(image_fpath=img_fpath_blur)

        self.assertGreater(value_sharp, value_blur)

    def test_AudioFile(self):
        mp3_fpath = join(tests_dir, 'test_data/music/test_us_and_them_short.mp3')
        audio = pydoni.AudioFile(mp3_fpath)

        # Method: compress()
        mp3_output = pydoni.append_filename_suffix(mp3_fpath, '-COMPRESSED')
        if isfile(mp3_output):
            remove(mp3_output)

        audio.compress(output_fpath=mp3_output)
        self.assertTrue(isfile(mp3_output))

        if isfile(mp3_output):
            remove(mp3_output)

        # Method: join() and get_duration() and export() (embedded within get_duration())
        mp3_fpath1 = join(tests_dir, 'test_data/music/test_us_and_them_short_first_half.m4a')
        mp3_fpath2 = join(tests_dir, 'test_data/music/test_us_and_them_short_second_half.m4a')

        audio = pydoni.AudioFile(mp3_fpath1)
        expected_output_fpath = pydoni.append_filename_suffix(mp3_fpath1, '-JOINED')

        if isfile(expected_output_fpath):
            remove(expected_output_fpath)

        audio.join(additional_audio_files=mp3_fpath2, output_fpath=expected_output_fpath)
        self.assertTrue(isfile(expected_output_fpath))

        audio = pydoni.AudioFile(expected_output_fpath)
        duration = audio.get_duration()
        expected_duration = 85
        self.assertEqual(int(duration), expected_duration)

        if isfile(expected_output_fpath):
            remove(expected_output_fpath)

        # Method: convert()
        m4a_fpath = join(tests_dir, 'test_data/music/test_us_and_them_short.m4a')
        mp3_output = splitext(m4a_fpath)[0] + '-CONVERTED.mp3'
        if isfile(mp3_output):
            remove(mp3_output)

        audio = pydoni.AudioFile(m4a_fpath)
        audio.convert(output_fpath=mp3_output, output_format='mp3')

        self.assertTrue(isfile(mp3_output))
        if isfile(mp3_output):
            remove(mp3_output)

        # Method: transcribe()
        # Uncomment when billing re-enabled https://console.cloud.google.com/billing
        # conversation_fpath = join(tests_dir, 'test_data/music/test_conversation.m4a')
        # audio = pydoni.AudioFile(conversation_fpath)
        # conversation_text = audio.transcribe()


tests_dir = dirname(abspath(__file__))
root_dir = dirname(tests_dir)
chdir(root_dir)

case = TestPydoni()

test_methods = [x for x in dir(case) if x.startswith('test_')]
for method in test_methods:
    getattr(case, method)()
