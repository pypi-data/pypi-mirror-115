__author__ = 'Andoni Sooklaris'
__email__ = 'andoni.sooklaris@gmail.com'


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


import ast
import click
import colr
import contextlib
import csv
import cv2
import datetime
import exiftool
import itertools
import inspect
import logging
import matplotlib
import matplotlib.cm
import numpy as np
import os
import pandas as pd
import pathlib
import pydoni
import PyInquirer as inq
import pytesseract
import re
import requests
import requests
import shutil
import sqlalchemy
import subprocess
import subprocess
import sys
import threading
import time
import typing
import wave
import zipfile
from bs4 import BeautifulSoup
from collections import defaultdict, OrderedDict
from dateutil.parser import parse
from dateutil.tz import tzoffset
from emoji import emojize
from google.cloud import speech
from lxml import html as lxml_html
from pandas.core.algorithms import isin
from PIL import Image, ImageFont, ImageDraw
from pydub import AudioSegment
from requests.exceptions import RequestException
from tqdm import tqdm, trange
from typing import Any
from xml.etree import ElementTree


# Module setup ---------------

module_loglevel = logging.ERROR


class ExtendedLogger(logging.Logger):
    """
    Extend the logging.Logger class.
    """
    def __init__(self, name, level=logging.NOTSET):
        self._count = 0
        self._countLock = threading.Lock()
        return super(ExtendedLogger, self).__init__(name, level)

    def var(self, varname, value, include_modules=True, include_extended_logger=True):
        """
        Extend .debug() method to log the name, value and datatype of a variable or variables.
        Optionally include modules and instances of this class. Functionally, this allows
        for iterating over `locals()` and automatically excluding modules and/or loggers
        from the logged output, instead leaving just the variables desired to be logged.

        For example, if `locals()` returns `{'a': 1, 'b': 2, 'logging': "<module 'logging' from..."}`

        The user can set `include_modules=False` to exclude the 'logging' module when iterating
        over `locals()`:

        >>> for k, v in locals().items():
        >>>     logger.var(k, v, include_modules=False)
        {timestamp} : DEBUG : __main__ : Variable 'a' {int}: 1
        {timestamp} : DEBUG : __main__ : Variable 'b' {int}: 2
        """
        dtype = value.__class__.__name__
        value = str(value)

        if dtype == 'module' and not include_modules:
            return None

        if 'ExtendedLogger' in dtype and not include_extended_logger:
            return None

        msg = f"Variable '{varname}' {{{dtype}}}: {value}"
        return super(ExtendedLogger, self).debug(msg)

    def logvars(self, var_dict):
        """
        Iterate over dictionary and call `self.var` on each variable name, variable value pair,
        excluding modules and instances of this class.
        """
        for varname, value in var_dict.items():
            self.var(varname, value, include_modules=False, include_extended_logger=False)


def logger_setup(name: str=__name__, level: int=logging.DEBUG, equal_width: bool=False):
    """
    Standardize logger setup across pydoni package.
    """
    logging.setLoggerClass(ExtendedLogger)
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger_fmt = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'

        if equal_width:
            logger_fmt = logger_fmt.replace('%(levelname)s', '%(levelname)-8s')

    formatter = logging.Formatter(logger_fmt)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(level)

    return logger


logger = logger_setup(name=__name__, level=module_loglevel, equal_width=False)


# Operating and file systems ---------------

class FinderMacOS(object):
    """
    MacOS Finder object. Holds functions to carry out Finder operations on a file or directory.
    """
    def __init__(self):
        self.mdls_bin = find_binary('mdls')
        self.has_mdls = self.mdls_bin is not None
        if not self.has_mdls:
            logger.warning('No `mdls` binary found, some command(s) may be unavailable')

        self.osascript_bin = find_binary('osascript')
        self.has_osascript = self.osascript_bin is not None
        if not self.has_osascript:
            logger.warning('No `osascript` binary found, some command(s) may be unavailable')

        self.tag_bin = find_binary('tag')
        self.has_tag = self.tag_bin is not None
        if not self.has_tag:
            logger.warning('No `tag` binary found, some command(s) may be unavailable')

    def get_comment(self, fpath: typing.Union[str, pathlib.Path]):
        """
        Call `mdls` BASH command to retrieve a file's Finder comment on macOS.
        """
        self.__require_binary__('mdls')

        cmd = f'{self.mdls_bin} -r -nullMarker "" -n kMDItemFinderComment "{fpath}"'
        res = syscmd(cmd, encoding='utf-8')

        if 'could not find' + os.path.basename(fpath) in res:
            raise Exception(f'Could not find Finder comment on file "{fpath}"')
        else:
            return res

    def write_comment(self, fpath: typing.Union[str, pathlib.Path], comment: str):
        """
        Use Applescript to write a Finder comment to a file.
        """
        self.__require_binary__('osascript')

        cmd = f'{self.osascript_bin} -e'

        applescript = '\n'.join([
            'set filepath to POSIX file "{file}"',
            'set the_file to filepath as alias',
            'tell application "Finder" to set the comment of the_file to "{comment}"'
        ])

        applescript_clear = applescript.format(file=fpath, comment='test')
        applescript_set = applescript.format(file=fpath, comment=comment)

        applescript_clear = re.sub(r'"', r'\"', applescript_clear)
        applescript_set = re.sub(r'"', r'\"', applescript_set)

        cmd_exec_clear = cmd + ' "' + applescript_clear + '"'
        syscmd(cmd_exec_clear)

        cmd_exec_set = cmd + ' "' + applescript_set + '"'
        syscmd(cmd_exec_set)

    def clear_comment(self, fpath: typing.Union[str, pathlib.Path]):
        """
        Use Applescript to remove a file's Finder comment.
        """
        self.__require_binary__('osascript')

        cmd = f'{self.osascript_bin} -e'

        applescript = '\n'.join([
            'set filepath to POSIX file "{file}"',
            'set the_file to filepath as alias',
            'tell application "Finder" to set the comment of the_file to "{comment}"'
        ])
        applescript = re.sub(r'"', r'\"', applescript)

        cmd_exec = cmd + ' "' + applescript + '"'

        # os.system(cmd_exec)
        syscmd(cmd_exec)
        return True

    def get_tag(self, fpath: typing.Union[str, pathlib.Path]):
        """
        Parse `mdls` output to get a file's Finder tags.
        """
        self.__require_binary__('mdls')

        cmd = f'{self.mdls_bin} -r -nullMarker "" -n kMDItemUserTags "{fpath}"'
        tags = syscmd(cmd, encoding='utf-8')

        if tags == '0':
            self.logger.warning(f'No tags found for file "{fpath}"')
            return []

        else:
            tags = [x.strip() for x in tags.split('\n') if '(' not in x and ')' not in x]
            tags = [x.replace(',', '') for x in tags]
            tags = ensurelist(tags)
            return tags

    def write_tag(self, fpath: typing.Union[str, pathlib.Path], tag: typing.Union[str, list]):
        """
        Write Finder tag or tags to a file. Requires Jdberry's 'tag' command line utility to
        be installed. Install from https://github.com/jdberry/tag
        """
        self.__require_binary__('tag')

        tag = ensurelist(tag)
        res = []
        for tg in tag:
            z = syscmd(f'{self.tag_bin} --add "{tg}" "{fpath}"')
            res.append(z)
        if len(list(set(res))) == 1:
            if list(set(res)) == [0]:
                return True
            else:
                return False
        else:
            return False

    def remove_tag(self, fpath: typing.Union[str, pathlib.Path], tag: typing.Union[str, list]):
        """
        Remove a Finder tag or tags from a file. Clear all tags by setting `tag='all'`.
        Requires that Jdberry's 'tag' command line utility is installed from

            https://github.com/jdberry/tag
        """
        self.__require_binary__('tag')

        tag = ensurelist(tag)

        if tag == ['all']:
            tag = self.get_tag(fpath)

        res = []
        for tg in tag:
            z = syscmd(f'{self.tag_bin} --remove "{tg}" "{fpath}"')
            res.append(z)

        if len(list(set(res))) == 1:
            if list(set(res)) == [0]:
                return True
            else:
                return False
        else:
            return False

    def clear_tags(self, fpath: typing.Union[str, pathlib.Path]):
        """
        Remove all Finder tags from a file.
        """
        self.__require_binary__('tag')

        existing_tags = self.get_tag(fpath)
        for tg in existing_tags:
            z = syscmd(f'{self.tag_bin} --remove "{tg}" "{fpath}"')

        return True


    def __require_binary__(self, bin_name):
        if not hasattr(self, 'has_' + bin_name):
            raise Exception(f'Could not find required `{bin_name}` binary')


def listfiles(path: typing.Union[str, pathlib.Path]='.',
              ext=None,
              pattern=None,
              ignore_case=True,
              full_names=False,
              recursive=False,
              include_hidden=True) -> list:
    """
    List files in a given directory.

    path {str} absolute path to search for files in
    ext {str} optional file extension or list of extensions to filter resulting files by
    pattern {str} optional filter resulting files by matching regex pattern
    ignore_case {bool} do not consider case in when filtering for `pattern` parameter
    full_names {bool} return absolute filepaths
    recursive {bool} search recursively down the directory tree
    include_hidden {bool} include hidden files in resulting file list
    """
    owd = os.getcwd()
    os.chdir(path)

    if recursive:
        fpaths = []
        for root, dpaths, filenames in os.walk('.'):
            for f in filenames:
                fpaths.append(os.path.join(root, f).replace('./', ''))
    else:
        fpaths = [f for f in os.listdir() if os.path.isfile(f)]

    if not include_hidden:
        fpaths = [f for f in fpaths if not os.path.basename(f).startswith('.')]

    if pattern is not None:
        if ignore_case:
            fpaths = [f for f in fpaths if re.search(pattern, f, re.IGNORECASE)]
        else:
            fpaths = [f for f in fpaths if re.search(pattern, f)]

    if ext:
        ext = [x.lower() for x in ensurelist(ext)]
        ext = ['.' + x if not x.startswith('.') else x for x in ext]
        fpaths = [x for x in fpaths if os.path.splitext(x)[1].lower() in ext]

    if full_names:
        path_expand = os.getcwd() if path == '.' else path
        fpaths = [os.path.join(path_expand, f) for f in fpaths]

    os.chdir(owd)
    return fpaths


def listdirs(path: typing.Union[str,
             pathlib.Path]='.',
             pattern: str=None,
             full_names: bool=False,
             recursive: bool=False) -> list:
    """
    List subdirectories in a given directory, optionally filtering by a regex pattern.
    """
    owd = os.getcwd()
    os.chdir(path)

    if recursive:
        dpaths = []
        for root, subdirs, filenames in os.walk('.'):
            for subdir in subdirs:
                dpaths.append(os.path.join(root, subdir).replace('./', ''))
    else:
        dpaths = [name for name in os.listdir('.') if os.path.isdir(os.path.join(path, name)) ]

    if full_names:
        path_expand = os.getcwd() if path == '.' else path
        dpaths = [os.path.join(path_expand, dname) for dname in dpaths]

    if pattern is not None:
        dpaths = [d for d in dpaths if re.match(pattern, d)]

    os.chdir(owd)
    return sorted(dpaths)


def systime(as_string: bool=True, compact: bool=False):
    """
    Get the current datetime, optionally formatted as a string.
    """
    if as_string:
        return datetime.datetime.now().strftime('%Y%m%d_%H%M%S' if compact else '%Y-%m-%d %H:%M:%S')
    else:
        assert not compact, 'Cannot set `compact` if returning a datetime object!'
        return datetime.datetime.now()


def sysdate(as_string: bool=True, compact: bool=False):
    """
    Get the current date, optionally formatted as a string.
    """
    if as_string:
        return datetime.datetime.now().strftime('%Y%m%d' if compact else '%Y-%m-%d')
    else:
        assert not compact, 'Cannot set `compact` if returning a datetime object!'
        return datetime.datetime.now().replace(hour=0, minute=0, second=0)


def human_filesize(nbytes: int):
    """
    Convert number of bytes to human-readable filesize string.
    Source: https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
    """
    base = 1

    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']:
        n = nbytes / base

        if n < 9.95 and unit != 'B':
            # Less than 10 then keep 1 decimal place
            value = '{:.1f} {}'.format(n, unit)
            return value

        if round(n) < 1000:
            # Less than 4 digits so use this
            value = f'{round(n)} {unit}'
            return value

        base *= 1024

    value = f'{round(n)} {unit}'

    return value


def textfile_len(fpath: typing.Union[str, pathlib.Path]):
    """
    Get number of rows in a text file.
    """
    with open(os.path.abspath(fpath)) as f:
        for i, l in enumerate(f):
            pass

    return i + 1


def dirsize(dpath: typing.Union[str, pathlib.Path]='.'):
    """
    Get size of directory in bytes.
    Source: https://stackoverflow.com/questions/1392413/calculating-a-directorys-size-using-python
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(dpath):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    logger.info(f'Total directory size of {dpath}: {total_size}')
    return total_size


def append_filename_suffix(fpath: typing.Union[str, pathlib.Path], suffix: str):
    """
    Add suffix string to filename before extension.
    """
    base, ext = os.path.splitext(fpath)

    if ext == '.icloud':
        ext_icloud = ext
        base, ext = os.path.splitext(base)
        ext += ext_icloud

    return base + suffix + ext


def time_machine_last_backup_info():
    """
    Get last update and last drive from tmutil latestbackup command.
    Return a tuple in format (drive name, last TM backup date)
    """
    tmutil_bin = find_binary('tmutil', abort=True)

    out = syscmd(f'{tmutil_bin} latestbackup', encoding='utf-8').strip()

    if 'Unable to locate' in out:
        logger.info('Queried for Time Machine last backup information')
        raise Exception('No known backup hard drive is connected')
    else:
        last_date = datetime.datetime.strptime(os.path.basename(out), '%Y-%m-%d-%H%M%S')
        last_date_str = last_date.strftime('%Y-%m-%d %H:%M:%S')
        last_drive = out.split('/Backups.backupdb')[0]
        logger.info('Queried for Time Machine last backup information')
        return (last_drive, last_date)


def time_machine_start():
    """
    Start Time Machine backup given path to `tmutil` binary if a known backup drive is connected.
    """
    tmutil_bin = find_binary('tmutil', abort=True)
    out = syscmd(f'{tmutil_bin} startbackup')
    logger.info('Started Time Machine backup')
    return out


def time_machine_stop():
    """
    Stop Time Machine backup given path to `tmutil` binary.
    """
    tmutil_bin = find_binary('tmutil', abort=True)
    out = syscmd(f'{tmutil_bin} stopbackup')
    logger.info('Stopped Time Machine backup')
    return out


def unarchive(zip_fpath: typing.Union[str, pathlib.Path], dest_dpath: typing.Union[str, pathlib.Path]='.'):
    """
    Unpack a .zip archive.
    """
    with zipfile.ZipFile(zip_fpath, 'r') as zip_ref:
        zip_ref.extractall(dest_dpath)

    logger.info(f'Extract zipfile "{zip_fpath}" to "{dest_dpath}"')


def macos_notify(message: str, *args, **kwargs):
    """
    Fire a macOS notification with custom configuration. Parameter 'message' is required,
    and remaining arguments are passed literally into the terminal-notifier tool.

    Source:
        https://github.com/julienXX/terminal-notifier
    """
    terminal_notifier_bin = find_binary('terminal-notifier', abort=True)

    # Build list of arguments for terminal-notifier and check that each parameter is valid
    assert isinstance(message, str), 'Paramter `message` must be a string'
    cmd_base = ['terminal-notifier']
    message_parameter = ['-message', message]
    additional_options = [['-' + k, f"{v}"] for k, v in kwargs.items()]
    additional_options = [item for sublist in additional_options for item in sublist]
    cmd = cmd_base + message_parameter + additional_options

    subprocess.call(cmd)
    logger.info(f'Fired macOS notification "{message}"')


def list_attached_volumes(external_only: bool=False) -> list:
    """
    List attached drives. If `external_only` is specified, filter the resulting list for
    only externally attached drives.
    """
    volumes = listdirs(os.path.join('/', 'Volumes'), full_names=True)

    if external_only:
        volumes = [v for v in volumes if os.path.basename(v) not in ['Macintosh HD', 'Recovery']]
        volumes = [v for v in volumes if 'com.' not in os.path.basename(v)]

    gerund = ' (externals only)' if external_only else ''
    logger.info(f'Found attached volumes{gerund}: {str(volumes)}')
    return volumes


def du_by_filetype(dpath: typing.Union[str, pathlib.Path],
                   recursive: bool=False,
                   quiet: bool=True,
                   human_readable: bool=False,
                   progress: bool=False,
                   total: bool=True):
    """
    List filesize of directory by filetype.

    dpath {str} path to directory to check
    recursive {bool} list files recursively
    quiet {bool} do not print output dictionary to console
    human_readable {bool} display filesize in output in human-readable format
    progress {bool} display progress bar while scanning directory
    total {bool} add final line to output with the total directory filesize
    """
    owd = os.getcwd()
    os.chdir(dpath)

    files = listfiles(recursive=recursive)
    filexts = list(set([os.path.splitext(f)[1].lower() for f in files]))
    extdict = {k: 0 for k in filexts}

    if progress:
        pbar = tqdm(total=len(files), unit='file')

    logger.info(f'Scanning {len(files)} in directory "{dpath}" all files and extracting total filesize by filetype')
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        extdict[ext] += os.stat(f).st_size
        if progress:
            pbar.update(1)

    if progress:
        pbar.close()

    # Define any extension name replacements. By default, '' is replaced with 'None'
    if '' in extdict.keys():
        extdict['None'] = extdict.pop('')

    # Order dictionary by filesize in descending order
    extdict = {k: v for k, v in sorted(extdict.items(), key=lambda item: item[1], reverse=True)}

    if total:
        extdict['total'] = sum([v for k, v in extdict.items()])

    if human_readable:
        extdict = {k: human_filesize(v) for k, v in extdict.items()}

    if not quiet:
        for ext, sizeb in extdict.items():
            print(ext + ' ' + str(sizeb))

    os.chdir(owd)
    return extdict


def excel_to_csv(excel_fpath: typing.Union[str, pathlib.Path], output_fpath=None):
    """
    Convert an Excel file with one or more sheets to a CSV file.
    """
    if output_fpath is None:
        output_fpath = os.path.splitext(excel_fpath)[0] + '.csv'

    xlsx = pd.ExcelFile(excel_fpath)
    sheets = xlsx.sheet_names

    if len(sheets) > 1:
        for sheet in sheets:
            data_xlsx = pd.read_excel(excel_fpath, sheet_name=sheet)
            tmpout = os.path.splitext(output_fpath)[0] + '-' + sheet + '.csv'
            data_xlsx.to_csv(tmpout, encoding='utf-8', index=False)
    else:
        logger.info('Writing single sheets')
        data_xlsx = pd.read_excel(excel_fpath)
        data_xlsx.to_csv(output_fpath, encoding='utf-8', index=False)

    logger.info(f'Converted Excel file "{excel_fpath}" to CSV "{output_fpath}"')


def remove_empty_subfolders(dpath: typing.Union[str, pathlib.Path], recursive: bool=False):
    """
    Scan a directory and delete any bottom-level empty directories.
    """
    owd = os.getcwd()
    os.chdir(dpath)

    removed = []

    if recursive:
        for root, dnames, fnames in os.walk('.', topdown=False):
            for dname in dnames:
                try:
                    os.rmdir(root)
                    removed.append(root)
                except OSError:
                    pass
    else:
        dpaths = [dname for dname in os.listdir('.') if os.path.isdir(os.path.join(dpath, dname))]
        for dname in dpaths:
            try:
                os.rmdir(dname)
                removed.append(dname)
            except OSError:
                pass

    if len(removed):
        logger.info(f'Deleted empty subdirectories of root "{dpath}": {str(removed)}')
    else:
        logger.info(f'No empty subdirectories of "{dpath}" found, none deleted')

    return removed


# Python object operations ---------------

def advanced_strip(string: str):
    """
    Strip whitespace off a string and replace all instances of >1 space with a single space.
    """
    return re.sub(r'\s+', ' ', string.strip())


def ensurelist(val: Any):
    """
    Accept a string or list and ensure that it is formatted as a list. If `val` is not a list,
    return [val]. If `val` is already a list, return as is.
    """
    return [val] if not isinstance(val, list) else val


def naturalsort(lst: list):
    """
    Sort a list with numeric elements, numerically.
    Source: https://stackoverflow.com/questions/5967500/how-to-correctly-sort-a-string-with-a-number-inside
    """
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        """
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        """
        return [atoi(c) for c in re.split(r'(\d+)', text)]

    return sorted(lst, key=natural_keys)


def listmode(lst: list):
    """
    Get the most frequently occurring value in a list.
    """
    return max(set(lst), key=lst.count)


def cap_nth_char(string: str, n: int):
    """
    Capitalize character in `string` at zero-indexed position `n`.

    Example:
        >>> cap_nth_char(string='string', n=3, replacement='I')
        'strIng'
    """
    return string[:n] + string[n].capitalize() + string[n+1:]


def replace_nth_char(string: str, n: int, replacement: str):
    """
    Replace character in `string` at zero-indexed position `n` with `replacement`.

    Example:
        >>> replace_nth_char(string='string', n=3, replacement='I')
        'strIng'
    """
    return string[:n] + str(replacement) + string[n+1:]


def insert_nth_char(string: str, n: int, char):
    """
    Insert `char` in `string` at zero-indexed position `n`.

    Example:
        >>> insert_nth_char(string='strng', n=3, char='I')
        'strIng'
    """
    return string [:n] + str(char) + string[n:]


def split_at(lst: list, idx: int):
    """
    Split `lst` at a single position or multiple positions denoted by `idx`. Every index value
    denoted in `idx` will be the *first* item of the subsequent sublist. Return a list of lists.

    Example:
        >>> split_at(lst=['a', 'b', 'c'], idx=1)
        [['a'], ['b', 'c']]
        # Element at position 1 is the first item of the second sublist
    """
    idx = ensurelist(idx)
    return [lst[i:j] for i, j in zip([0] + idx, idx + [None])]


def duplicated(lst: list):
    """
    Return list of boolean values indicating whether each item in a list is a duplicate of
    a previous item in the list. Order matters!
    """
    dup_ind = []

    for i, item in enumerate(lst):
        tmplist = lst.copy()
        del tmplist[i]

        if item in tmplist:
            # Test if this is the first occurrence of this item in the list. If so, do not
            # count as duplicate, as the first item in a set of identical items should not
            # be counted as a duplicate

            first_idx = min(
                [i for i, x in enumerate(tmplist) if x == item])

            if i != first_idx:
                dup_ind.append(True)
            else:
                dup_ind.append(False)

        else:
            dup_ind.append(False)

    return dup_ind


def test_value(value: Any, dtype: str, return_coerced_value: bool=False, stop: bool=False):
    """
    Test if a value is an instance of type `dtype`. May accept a value of any kind.

    Parameter `dtype` must be one of ['bool', 'str', 'string', 'int', 'integer',
    'float', 'date', 'datetime', 'path', 'path exists'].

    Parameter `return_coerced_value` will cause this function to return `value` as type
    `dtype` if possible, and will raise an error otherwise.

    Parameter `stop` will cause this function to raise an error if `value` cannot be
    coerced to `dtype` instead of simply logging the error message.
    """
    class Attribute():
        """
        Empty class defined for convenient use.
        """
        pass

    def define_date_regex():
        """
        Define regex strings for all valid date components.
        """
        rgx = Attribute()
        rgx.sep = r'(\.|\/|-|_|\:)'

        rgx.year = r'(?P<year>\d{4})'
        rgx.month = r'(?P<month>\d{2})'
        rgx.day = r'(?P<day>\d{2})'

        rgx.hour = r'(?P<hour>\d{2})'
        rgx.minute = r'(?P<minute>\d{2})'
        rgx.second = r'(?P<second>\d{2})'
        rgx.microsecond = r'(?P<microsecond>\d+)'

        rgx.tz_sign = r'(?P<tz_sign>-|\+)'
        rgx.tz_hour = r'(?P<tz_hour>\d{1,2})'
        rgx.tz_minute = r'(?P<tz_minute>\d{1,2})'

        rgx.date = f'{rgx.year}{rgx.sep}{rgx.month}{rgx.sep}{rgx.day}'
        rgx.datetime = fr'{rgx.date} {rgx.hour}{rgx.sep}{rgx.minute}{rgx.sep}{rgx.second}'
        rgx.datetime_timezone = fr'{rgx.datetime}{rgx.tz_sign}{rgx.tz_hour}(:){rgx.tz_minute}'
        rgx.datetime_microsecond = fr'{rgx.datetime}(\.){rgx.microsecond}'

        return rgx

    def anchor(x):
        """
        Add regex start and end anchors to a string.
        """
        return '^' + x + '$'


    valid_dtypes = ['bool',
                    'str', 'string',
                    'int', 'integer',
                    'float',
                    'date',
                    'datetime',
                    'path',
                    'path exists']
    assert dtype in valid_dtypes, f"Datatype must be one of {', '.join(valid_dtypes)}"

    # Date/datetime regex definitions
    rgx = define_date_regex()

    coerced_value = None

    # Test bool
    if dtype == 'bool':
        if isinstance(value, bool):
            coerced_value = value
        else:
            if str(value).lower() in ['true', 't', 'yes', 'y']:
                coerced_value = True
            elif str(value).lower() in ['false', 'f', 'no', 'n']:
                coerced_value = False

    # Test string
    elif dtype in ['str', 'string']:
        try:
            coerced_value = str(value)
        except Exception as e:
            if stop:
                raise e
            else:
                logger.warning(str(e))

    # Test integer
    elif dtype in ['int', 'integer']:
        if isinstance(value, int):
            coerced_value = value
        elif str(value).isdigit():
            coerced_value = int(value)
        else:
            try:
                coerced_value = int(value)
            except Exception as e:
                if stop:
                    raise e
                else:
                    logger.warning(str(e))

    # Test float
    elif dtype == 'float':
        if isinstance(value, float) or isinstance(value, int):
            coerced_value = float(value)
        elif '.' in str(value):
            try:
                coerced_value = float(value)
            except Exception as e:
                if stop:
                    raise e
                else:
                    logger.warning(str(e))

    # Test date
    elif dtype == 'date':
        m = re.search(anchor(rgx.date), str(value).strip())
        if m:
            dt_components = dict(year=m.group('year'), month=m.group('month'), day=m.group('day'))
            dt_components = {k: int(v) for k, v in dt_components.items()}
            coerced_value = datetime.datetime(**dt_components)

    # Test datetime
    elif dtype == 'datetime':
        m_dt = re.search(anchor(rgx.datetime), str(value).strip())
        m_dt_tz = re.search(anchor(rgx.datetime_timezone), str(value).strip())
        m_dt_ms = re.search(anchor(rgx.datetime_microsecond), str(value).strip())

        if m_dt:
            dt_components = dict(year=m_dt.group('year'),
                                 month=m_dt.group('month'),
                                 day=m_dt.group('day'),
                                 hour=m_dt.group('hour'),
                                 minute=m_dt.group('minute'),
                                 second=m_dt.group('second'))
            dt_components = {k: int(v) for k, v in dt_components.items()}
            coerced_value = datetime.datetime(**dt_components)

        elif m_dt_tz:
            dt_components = dict(year=m_dt_tz.group('year'),
                                 month=m_dt_tz.group('month'),
                                 day=m_dt_tz.group('day'),
                                 hour=m_dt_tz.group('hour'),
                                 minute=m_dt_tz.group('minute'),
                                 second=m_dt_tz.group('second'))
            dt_components = {k: int(v) for k, v in dt_components.items()}

            second_offset = int(m_dt_tz.group('tz_hour')) * 60 * 60
            second_offset = -second_offset if m_dt_tz.group('tz_sign') == '-' else second_offset

            dt_components['tzinfo'] = tzoffset(None, second_offset)
            coerced_value = datetime.datetime(**dt_components)

        elif m_dt_ms:
            dt_components = dict(year=m_dt_ms.group('year'),
                                 month=m_dt_ms.group('month'),
                                 day=m_dt_ms.group('day'),
                                 hour=m_dt_ms.group('hour'),
                                 minute=m_dt_ms.group('minute'),
                                 second=m_dt_ms.group('second'),
                                 microsecond=m_dt_ms.group('microsecond'))
            dt_components = {k: int(v) for k, v in dt_components.items()}
            coerced_value = datetime.datetime(**dt_components)

    # Test path
    elif dtype == 'path':
        if '/' in value or value == '.':
            coerced_value = value

    # Test path exists
    elif dtype == 'path exists':
        if os.path.isfile(value) or os.path.isdir(value):
            coerced_value = value

    # Close function
    if coerced_value is None:
        error_str = f"Unable to coerce value '{str(value)}' (dtype: {type(value).__name__}) to {dtype}"
        logger.warning(error_str)

        if return_coerced_value:
            raise ValueError(error_str)
        else:
            return False

    else:
        if return_coerced_value:
            return coerced_value
        else:
            return True


def fmt_seconds(time_in_sec: int, units: str='auto', round_digits: int=4):
    """
    Format time in seconds to a custom string. `units` parameter can be
    one of 'auto', 'seconds', 'minutes', 'hours' or 'days'.
    """
    if units == 'auto':
        if time_in_sec < 60:
            time_diff = round(time_in_sec, round_digits)
            time_measure = 'seconds'
        elif time_in_sec >= 60 and time_in_sec < 3600:
            time_diff = round(time_in_sec/60, round_digits)
            time_measure = 'minutes'
        elif time_in_sec >= 3600 and time_in_sec < 86400:
            time_diff = round(time_in_sec/3600, round_digits)
            time_measure = 'hours'
        else:
            time_diff = round(time_in_sec/86400, round_digits)
            time_measure = 'days'

    elif units in ['seconds', 'minutes', 'hours', 'days']:
        time_measure = units
        if units == 'seconds':
            time_diff = round(time_in_sec, round_digits)
        elif units == 'minutes':
            time_diff = round(time_in_sec/60, round_digits)
        elif units == 'hours':
            time_diff = round(time_in_sec/3600, round_digits)
        else:
            # Days
            time_diff = round(time_in_sec/86400, round_digits)

    return dict(zip(['units', 'value'], [time_measure, time_diff]))


def collapse_df_columns(df: pd.DataFrame, sep: str='_'):
    """
    Collapse a multi-level column index in a dataframe.
    """
    df.columns = [sep.join(col).strip() for col in df.columns.values]
    return df


def extract_colorpalette(palette_name: str, n: int=None, mode: str='hex'):
    """
    Convert color palette to color ramp list.

    palette_name {str} name of color palette
    n {int} size of color ramp. If None, automatically return the maximum number of colors in the color palette
    mode {str} type of colors to return, one of ['rgb', 'hex', 'ansi']
    """
    assert mode in ['rgb', 'hex', 'ansi']

    if n is None:
        cmap_mpl = matplotlib.cm.get_cmap(palette_name)
    else:
        cmap_mpl = matplotlib.cm.get_cmap(palette_name, n)

    cmap = dict(rgb=OrderedDict(), hex=OrderedDict(), ansi=OrderedDict())

    for i in range(cmap_mpl.N):
        rgb = cmap_mpl(i)[:3]
        hex = matplotlib.colors.rgb2hex(rgb)
        ansi = colr.color('', fore=hex)
        cmap['rgb'].update({rgb: None})
        cmap['hex'].update({hex: None})
        cmap['ansi'].update({ansi: None})

    target = [x for x, _ in cmap[mode].items()]

    if isinstance(n, int):
        if n > len(target):
            rep = int(np.floor(n / len(target)))
            target = list(itertools.chain.from_iterable(itertools.repeat(x, rep) for x in target))
            target += [target[-1]] * (n - len(target))

    return target


def rename_dict_keys(dct: dict, key_dict: dict):
    """
    Rename dictionary keys using a `key_dict` mapping.
    """
    for k, v in key_dict.items():
        if k in dct.keys():
            dct[v] = dct.pop(k)

    return dct


# Verbosity ---------------

class Verbose(object):
    """
    Handle verbose printing to console for pydoni-cli commands. Has advantage of accepting
    a 'verbose' parameter, then not printing if that is False, similar to logging behavior.
    """
    def __init__(self, verbose: bool=True, debug: bool=False, timestamp: bool=False):
        self.verbose = verbose
        self.debug_flag = debug
        self.timestamp = timestamp
        self.pbar = None

    def echo(self, *args, **kwargs):
        if self.verbose:
            echo(*args, **kwargs)

    def debug(self, *args, **kwargs):
        if self.debug_flag:
            kwargs['level'] = 'debug'
            echo(*args, **kwargs)

    def info(self, *args, **kwargs):
        if self.verbose:
            kwargs['level'] = 'info'
            echo(*args, **kwargs)

    def warn(self, *args, **kwargs):
        if self.verbose:
            kwargs['level'] = 'warn'
            echo(*args, **kwargs)

    def error(self, *args, **kwargs):
        if self.verbose:
            kwargs['level'] = 'error'
            echo(*args, **kwargs)

    def line_break(self):
        if self.verbose:
            print()

    def section_header(self, msg: str, time_in_sec: int=None, round_digits: int=2):
        """
        Print STDOUT verbose section header and optionally print the estimated time
        that the following section of code is expected to take
        """
        header = click.style(msg, fg='white', bold=True)

        # If time in seconds is given, augment header to incorporate estimated time
        if isinstance(time_in_sec, int) or isinstance(time_in_sec, float):
            # Get estimated time as dictionary
            est_time = fmt_seconds(time_in_sec=time_in_sec, units='auto', round_digits=round_digits)
            header = advanced_strip(f"""
            {header}
            {click.style('->', fg='white', bold=True)}
            Est. time
            {click.style(str(est_time['value']) + ' ' + est_time['units'], fg='yellow', bold=True)}
            """)

        echo(header)

    def program_complete(self,
                         msg: str='Program complete',
                         emoji_string: str=':rocket:',
                         start_ts: typing.Union[float, datetime.datetime]=None):
        """
        Print 'program complete' message intended to be use at script or program completion.
        """
        if self.verbose:
            emoji_string = ':' + emoji_string.replace(':', '') + ':'
            emoji_string = emojize(emoji_string, use_aliases=True)

            if isinstance(start_ts, datetime.datetime) or isinstance(start_ts, int):
                if isinstance(start_ts, datetime.datetime):
                    end_ts = datetime.datetime.now()
                    diff_in_seconds = (end_ts - start_ts).microseconds / 100000
                elif isinstance(start_ts, int):
                    end_ts = time.time()
                    diff_in_seconds = end_ts - start_ts

                diff_formatted = fmt_seconds(diff_in_seconds, units='auto', round_digits=2)
                elapsed_time = f"{diff_formatted['value']} {diff_formatted['units']}"
                elapsed_time = 'Elapsed time: ' + elapsed_time + ' '
            else:
                elapsed_time = ''

            msg = f'\n[ {msg} {emoji_string} {elapsed_time}]'
            print(msg)

    def pbar_init(self, *args, **kwargs):
        if self.verbose:
            self.pbar = tqdm(*args, **kwargs)

    def pbar_update(self, n):
        if self.verbose:
            self.pbar.update(n)

    def pbar_write(self, msg: str, refer_debug: bool=False):
        """
        Write to `self.pbar`. If `refer_debug` is True, then only write if `self.debug_flag`
        is also True. Otherwise, simply write if `self.verbose` is True. This functionality
        is useful when writing from the progress bar is desired only in debug mode, but
        not necessarily in verbose mode.
        """
        if refer_debug:
            if self.debug_flag:
                tqdm.write(msg)
        else:
            if self.verbose:
                tqdm.write(msg)

    def pbar_close(self):
        if self.verbose:
            self.pbar.close()

    def pbar_log_inline(self, msg_lst):
        """
        Print list of strings below TQDM progress bar.
        """
        for i, m in enumerate(msg_lst, 1):
            trange(1, desc=str(m), position=i, bar_format='{desc}')


def print_apple_ascii_art(by_line: bool=False, by_char: bool=False, sleep: int=0):
    """
    Print Apple WWDC 2016 ASCII artwork logo.
    """
    ascii_string = '\n'.join([
        '                                  -·',
        '                              _/=\\:<',
        '                             .#/*let}',
        '                           //as\\@#:~/',
        '                          try()|:-./',
        '                         *~let:>@f#',
        '                         </>#@~*/',
        '                        (+!:~/+/',
        '                        /={+|',
        '          _.:+*as=._           _.]@~let[._',
        '       .*()/if{@[[-#>\\=.__.<>/#{*+/@*/for=*~.',
        '      /-(#]:.(var/@~as/@</>\\]=/<if[/*:/<try@\\~',
        '     [:/@#</>}#for=\\>.<:try#>=\\*.if(var<<.+_:#(=.',
        '   #do()=*:.>as//@[]-./[#=+)\\(var/@<>[]:-##~/*>',
        '  =*:/([<.//>*~/]\\+/_/([\\<://:_*try/<:#if~do-:',
        ' @#/*-:/#do.i@var=\\<)]#>/=\\>\\<for#>|*:try=\"</',
        ' :/./@#[=#@-asl#:/-i@if.>#[.)=*>/let\\{\\}</):',
        ' (@+_let#do/.@#=#>[/]#let=#or@\\=<()~if)*<)\\)',
        'for):/=]@#try:</=*;/((+do_{/!\\"(@-/((:@>).*',
        '/@#:@try*@!\\as=\\>_@.>#+var>_@=>#+-do)=+@#>(',
        '{}:/./@#=do]>/@if)=[/[!\\<)#)try+*:~/#).=})=',
        'try@#_<(=<i>do#.<}@#}\\\\=~*:/().<))_+@#()+\\>',
        ' *:#for@:@>):/#<\\=*>@\\var_}#|[/@*-/.<:if#/-\\',
        ' =<)=~\\(-for>ii@if*=*+#as\\<)*:#for@f#)try+}).',
        ' [for()=.[#in=*:as=\\>_@-.>#do/:/([+var)=+@#]]=',
        '  /@[as:=\\+@#]=:/let[(=\\<_)</@->#for()=))#>in>)_',
        '  *)\\{}/*<var/(>;<+/:do#/-)<\\(:as/>)(})_+=<(for+=\\.',
        '   do=~\\@#=\\><<-))_|@#(])/)_+@let]:[+#\\=@/if[#()[=',
        '    =<]).if|/.=*@var<@:/(-)=*:/#)=*>@#var(<(]if):*',
        '    {/+_=@#as}#:/-i@if>in=@#{#in=>()@>](@#<{:})->',
        '     \\.=let_@<)#)_=\\<~#_)@}+@if#-[+#\\|=@#~try/as',
        '       var<:))+-ry-#»+_+=)>@#>()<?>var)=~<+.-/',
        '        +@>#do(as)*+[#]=:/(/#\\<)if).+let:@(.#\"',
        '         {}</().try()##/as<){*-</>}](as*>-/<',
        '           <()if}*var(<>.-\"_\"~.let>#[.)=*>/',
        '             {}<as:\"            \"*)}do>',
    ])

    if by_line or by_char:
        if by_line and by_char:
            logger.warning('Both `by_line` and `by_char` specified. Prioritizing `by_line`.')

        if by_line:
            lines = ascii_string.split('\n')
            for line in lines:
                print(line)
                if sleep > 0:
                    time.sleep(sleep)

        elif by_char:
            for char in ascii_string:
                print(char, end='', flush=True)
                if sleep > 0:
                    time.sleep(sleep)
    else:
        print(ascii_string)


def echo(msg: str,
         indent: int=0,
         timestamp: bool=False,
         level: str='T',
         arrow: str=None,
         capture_output: bool=False,
         **kwargs):
    """
    Update stdout with custom message and many custom parameters including indentation,
    timestamp, warning/error message, text styles, and more!

    msg {str} message to print to console
    indent {int} indentation level of message printed to console
    timestamp {bool} print datetimestamp preceding message
    return_str {bool} return string instead of printing
    arrow {str} color of arrow to display before message
    capture_output {bool} return the printed message as a stirng
    """
    msg = click.style(msg, **kwargs)
    ts = systime(as_string=True) if timestamp else ''
    indent_str = '  ' * indent
    arrow_str = click.style('==> ', fg=arrow, bold=True) if arrow else ''

    # Add preceding colored string for specified keyword args
    letter_map = dict(SUCCESS='S',
                      TEXT='T',
                      DEBUG='D',
                      INFO='I',
                      WARN='W',
                      ERROR='E',
                      FATAL='F')
    letter_map_rev = {v: k for k, v in letter_map.items()}
    color_map = dict(S='green', T='white', D='white', I='white', W='yellow', E='red', F='red')

    level = level.upper()
    if len(level) == 1:
        level_long = letter_map_rev[level]
        level_short = level
    else:
        level_short = letter_map[level]
        level_long = level

    classic_levels = ['D', 'I', 'W', 'E']  # logging module DEBUG/INFO/WARNING/ERROR
    custom_levels = ['S', 'F']  # Custom levels that should be included in message

    # Build message prefix (timestamp, level)
    if timestamp:
        if level_short in classic_levels:
            prefix = f'[{ts} {level_short}] '
        elif level_short in custom_levels:
            prefix = f'[{ts}] {level_long + ": "}'
        else:
            prefix = f'[{ts}] '
    else:
        if level_short in classic_levels:
            prefix = f'[{level_short}] '
        elif level_short in custom_levels:
            prefix = f'{level_long + ": "}'
        else:
            prefix = ''

    # Colorize message prefix based on `level`
    prefix_color = color_map[level_short]
    if prefix_color != 'white':
        prefix = click.style(prefix, fg=color_map[level_short])

    # Build infix (indent, arrow)
    infix = indent_str + arrow_str

    # Combine into final message
    output_msg = f'{prefix}{infix}{msg}'
    click.echo(output_msg)

    if capture_output:
        return output_msg


def print_columns(lst, ncol: int=2, delay: int=None):
    """
    Print a list as side-by-side columns.
    """
    def chunks(lst, chunk_size):
        """
        Split a list into a list of lists.

        lst {list} list to split

        chunk_size {int} size of chunks

        """
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

    lstlst = list(chunks(lst, ncol))
    col_width = max(len(word) for row in lstlst for word in row) + 2

    for row in lstlst:
        print(''.join(word.ljust(col_width) for word in row))

        if delay is not None:
            if delay > 0:
                time.sleep(delay)


def stabilize_postfix(key, max_len: int=20, fillchar: str='•', side: str='right'):
    """
    Create "stabilized" postfix (of consistent length) to be fed into
    a tqdm progress bar. This ensures that the postfix is always of
    a certain length, which causes the tqdm progress bar to be stable
    rather than moving left to right when keys of length smaller
    than `max_len` are encountered.

    key {str} string to set as postfix
    max_len {int} length of postfix
    fillchar {str} character to fill any spaces on the left with
    side {str} which side of postfix substring to keep, one of ['left', 'right']
    """
    if side == 'left':
        postfix = key[0:max_len].ljust(max_len, fillchar)
    elif side == 'right':
        postfix = key[-max_len:].rjust(max_len, fillchar)

    m = re.match(r'^ +', postfix)
    if m:
        leading_spaces = m.group(0)
        postfix = re.sub(r'^ +', fillchar * len(leading_spaces), postfix)

    m = re.match(r' +$', postfix)
    if m:
        trailing_spaces = m.group(0)
        postfix = re.sub(r'^ +', fillchar * len(trailing_spaces), postfix)

    return postfix


# Bash command wrappers ---------------

class EXIF(object):
    """
    Extract and operate on EXIF metadata from a media file or multiple files. Wrapper for
    `exiftool` by Phil Harvey system command.
    """
    def __init__(self, fpath: typing.Union[str, pathlib.Path]):
        self.fpath = pydoni.ensurelist(fpath)
        self.fpath = [os.path.abspath(f) for f in self.fpath]
        for f in self.fpath:
            assert os.path.isfile(f), f'File "{f}" does not exist'

        self.is_batch = len(self.fpath) > 1
        self.exiftool_bin = find_binary('exiftool', abort=True)
        logger.info(f'Found exiftool binary "{self.exiftool_bin}"')

    def extract(self, method: str='doni', clean_keys: bool=False, clean_values: bool=False):
        """
        Extract EXIF metadata from file or files. Parameter `method` may be one of
        'doni' or 'pyexiftool'. The `clean_*` toggles will apply `self.clean_keys()` and/or
        `self.clean_values()` respectively to the output metadata dictionary.
        """
        assert method in ['doni', 'pyexiftool']

        def split_cl_filenames(fpaths: typing.Union[str, pathlib.Path],
                               char_limit: int,
                               exiftool_bin: typing.Union[str, pathlib.Path]):
            """
            Determine at which point to split list of filenames to comply with command-line
            character limit, and split list of filenames into list of lists, where each sublist
            represents a batch of files to run `exiftool` on, where the entire call to `exiftool`
            for that batch will be under the maximum command-line character limit. Files must
            be broken into batches if there are too many to fit on in command-line command,
            because the `exiftool` syntax is as follows:

            exiftool filename_1 filename_2 filename_3 ... filename_n

            With too many files, the raw length of the call to `exiftool` might be over the
            character limit.
            """
            split_idx = []
            count = 0

            # Get character length of each filename
            str_lengths = [len(x) for x in fpaths]

            # Get indices to split at depending on character limit
            for i in range(len(str_lengths)):
                # Account for two double quotes and a space
                val = str_lengths[i] + 3
                count = count + val
                if count > char_limit - len(exiftool_bin + ' '):
                    split_idx.append(i)
                    count = 0

            # Split list of filenames into list of lists at the indices gotten in
            # the previous step
            return split_at(fpaths, split_idx)

        def etree_to_dict(t):
            """
            Convert XML ElementTree to dictionary.

            Source: https://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree
            """
            d = {t.tag: {} if t.attrib else None}
            children = list(t)

            if children:
                dd = defaultdict(list)
                for dc in map(etree_to_dict, children):
                    for k, v in dc.items():
                        dd[k].append(v)
                d = {t.tag: {k: v[0] if len(v) == 1 else v
                             for k, v in dd.items()}}

            if t.attrib:
                d[t.tag].update(('@' + k, v)
                                for k, v in t.attrib.items())

            if t.text:
                text = t.text.strip()
                if children or t.attrib:
                    if text:
                      d[t.tag]['#text'] = text
                else:
                    d[t.tag] = text

            return d

        def unnest_http_keynames(d):
            """
            Iterate over dictionary and test for key:value pairs where `value` is a
            dictionary with a key name in format "{http://...}". Iterate down until the
            terminal value is retrieved, then return that value to the original key name `key`
            """
            tmpd = {}

            for k, v in d.items():
                while isinstance(v, dict) and len(v) == 1:
                    key = list(v.keys())[0]
                    if re.search(r'\{http:\/\/.*\}', key):
                        v = v[key]
                    else:
                        break

                tmpd[k] = v

            return tmpd

        if method == 'doni':
            if not len(self.fpath):
                return {}

            num_files = len(self.fpath)
            logger.info(f'Extracting EXIF metadata for {num_files} files')

            char_limit = 50000

            file_batches = split_cl_filenames(self.fpath, char_limit, self.exiftool_bin)
            logger.info(f'Split {num_files} file(s) into {len(file_batches)} batch(es)')

            commands = []
            for batch in file_batches:
                cmd = self.exiftool_bin + ' -xmlFormat ' + ' '.join(['"' + f + '"' for f in batch]) + ' ' + '2>/dev/null'
                commands.append(cmd)

            exifd = {}
            for i, cmd in enumerate(commands):
                logger.info(f'Running batch {i+1} of {len(file_batches)} containing {len(file_batches[i])} total files')

                try:
                    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    xmlstring, err = proc.communicate()
                    xmlstring = xmlstring.decode('utf-8')
                except Exception as e:
                    logger.exception(f'Unable to execute system command: {cmd}')
                    raise e

                try:
                    root = ElementTree.fromstring(xmlstring)
                    elist = etree_to_dict(root)
                    elist = elist['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF']
                    elist = elist['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description']
                    if isinstance(elist, dict):
                        elist = [elist]

                except Exception as e:
                    logger.info('Unable to coerce ElementTree to dictionary')
                    raise e

                for d in elist:
                    tmpd = {}

                    # Clean dictionary keys in format @{http://...}KeyName
                    for k, v in d.items():
                        new_key = re.sub(r'@?\{.*\}', '', k)
                        tmpd[new_key] = v

                    # Unnest nested dictionary elements with "http://..." as the keys
                    tmpd = unnest_http_keynames(tmpd)

                    fnamekey = os.path.join(tmpd['Directory'], tmpd['FileName'])
                    exifd[fnamekey] = tmpd

                del elist


            if clean_keys:
                exifd = self.clean_keys(exifd)
                logger.info('Cleaned EXIF dictionary keys')

            if clean_values:
                exifd = self.clean_values(exifd)
                logger.info('Cleaned EXIF dictionary values')

            logger.info('EXIF metadata extraction complete')
            return exifd

        elif method == 'pyexiftool':
            with exiftool.ExifTool() as et:
                if self.is_batch:
                    exifd = et.get_metadata_batch(self.fpath)
                else:
                    exifd = et.get_metadata(self.fpath)

            return exifd

    def write(self, attrs: dict):
        """
        Write EXIF attribute(s) on a file or list of files, specified in key:value pairs of
        attr_name: desired_attr_value.
        """
        for k, v in attrs.items():
            self.__is_valid_tag_name__(k)

        tracker = {}
        for fpath in self.fpath:
            for tag_name, tag_value in attrs.items():
                default_cmd = f'{self.exiftool_bin} -overwrite_original -{tag_name}="{str(value)}" "{fpath}"'

                # Handle any special tag_name cases
                if tag_name == 'Keywords':
                    # Must be written in format:
                    #     exiftool -keywords=one -keywords=two -keywords=three FILE
                    # Otherwise, comma-separated keywords will be written as a single string
                    if isinstance(value, str):
                        if ',' in value:
                            value = value.split(', ')

                    if isinstance(value, list):
                        if len(value) > 1:
                            kwd_cmd = ' '.join(['-keywords="' + str(x) + '"' for x in value])

                    if 'kwd_cmd' in locals():
                        cmd = f'{self.exiftool_bin} -overwrite_original {kwd_cmd} "{fpath}"'
                    else:
                        cmd = default_cmd

                else:
                    cmd = default_cmd

                res = syscmd(cmd, encoding='utf-8')

                # Make sure that tag was appropriately set on `fpath`
                if self.__is_valid_tag_message__(res):
                    logger.info(f'File "{fpath}" set tag "{tag_name}" to value "{tag_value}"')
                    tracker[fpath] = True
                else:
                    logger.error(f'File "{fpath}" failed to set tag "{tag_name}" to value "{tag_value}" but exiftool system command did not throw an error')
                    tracker[fpath] = False

        return tracker

    def remove(self, tags: typing.Union[str, list]):
        """
        Remove EXIF attribute from a file or list of files.
        """
        tags = ensurelist(tags)
        for tag in tags:
            self.__is_valid_tag_name__(tag)

        for file in self.fpath:
            logger.info("File: " + file)

            for tag in tags:
                cmd = '{} -overwrite_original -{}= "{}"'.format(self.exiftool_bin, tag, file)

                try:
                    logger.var('cmd', cmd)
                    res = syscmd(cmd, encoding='utf-8')
                    logger.var('res', res)

                    if self.__is_valid_tag_message__(res):
                        logger.info("Success. Tag: %s" % tag)
                    else:
                        logger.error("ExifTool Error. Tag: %s" % tag)
                        logger.debug('ExifTool output: %s' % str(res))

                except Exception as e:
                    logger.exception("Failed. Tag: %s" % tag)
                    raise e

    def clean_values(self, exifd: dict):
        """
        Attempt to coerce EXIF values to Python data structures where possible. Try to coerce
        numerical values to Python int or float datatypes, dates to Python datetime values,
        and so on.

        Example:
            >>> EXIF().clean_values({
            >>>     'sample_int_pos': '+7',
            >>>     'sample_int_neg': '-7',
            >>>     'sample_dt_colon': '2018:02:29 01:28:10',
            >>>     'sample_dt_correct': '2018-02-29 01:28:10',
            >>>     'sample_float': '11.11',
            >>> })
            {
                'sample_int_pos': 7,
                'sample_int_neg': -7,
                'sample_dt_colon': '2018-02-29 01:28:10',
                'sample_dt_correct': '2018-02-29 01:28:10',
                'sample_float': 11.11,
            }
        """
        def detect_dtype(val: Any):
            """
            Wrap `pydoni.test()` in the context of EXIF metadata cleaning. Acceptable
            return values are ['bool', 'float', 'int', 'date', 'datetime', 'str'].
            """
            valid_dtypes = ['bool', 'float', 'int', 'datetime', 'date', 'str']
            for dtype in valid_dtypes:
                if dtype == 'str':
                    return dtype
                else:
                    if test_value(val, dtype):
                        return dtype

            # 'Otherwise' condition
            return 'str'

        newexifd = {}
        for fpath, d in exifd.items():
            newexifd[fpath] = {}

            for k, v in d.items():
                dtype = detect_dtype(v)
                if dtype in ['bool', 'date', 'datetime', 'int', 'float']:
                    coerced_value = test_value(v, dtype, return_coerced_value=True)
                    if v != coerced_value:
                        newexifd[fpath][k] = coerced_value
                        continue

                # Accounts for str values
                newexifd[fpath][k] = v

        return newexifd

    def clean_keys(self, exifd: dict):
        """
        Clean EXIF element names.
        """
        column_map_json_fpath = os.path.join(os.path.dirname(__file__), 'data', 'exif_column_map.json')
        with open(column_map_json_fpath, 'r') as f:
            column_map = ast.literal_eval(f.read())

        newd = {}
        not_found_keys = []

        for fpath, dct in exifd.items():
            newd[fpath] = rename_dict_keys(dct, column_map)
            for exif_key in newd[fpath].keys():
                if exif_key not in column_map.keys() and exif_key not in column_map.values():
                    logger.warning(f'No mapped name found for key {exif_key} in {column_map_json_fpath}, key not renamed and left as-is')
                    not_found_keys.append(exif_key)

        if not_found_keys:
            # Key(s) not in above column map, this means we must rename them manually from
            # ExifKeyName to exif_key_name.
            new_keynames = []
            for key in not_found_keys:
                new_key = ''
                for i, char in enumerate(key):
                    if char == char.upper() and not char.isdigit() and i > 0:
                        new_key += '_' + char
                    else:
                        new_key += char

                # Corrections
                new_key = new_key.lower()
                new_key = new_key.replace('i_d', 'id')

                new_keynames.append(new_key)

            newd[fpath] = rename_dict_keys(newd[fpath], dict(zip(not_found_keys, new_keynames)))

        return newd

    def __is_valid_tag_name__(self, tags: typing.Union[str, list]):
        """
        Check EXIF tag names for illegal characters.
        """
        tags = ensurelist(tags)
        illegal_chars = ['-', '_']
        for tag in tags:
            for char in illegal_chars:
                if char in tag:
                    raise Exception(f'Illegal character "{char}" in tag name "{tag}"')

        return True

    def __is_valid_tag_message__(self, tagmsg: str):
        """
        Determine if EXIF write was successful based on tag message.
        """
        if 'nothing to do' in tagmsg.lower():
            return False
        else:
            return True


class AudioFile(object):
    """
    Wrapper for FFmpeg BASH commands.
    """
    def __init__(self, audio_fpath):
        self.fpath = os.path.abspath(audio_fpath)
        self.ext = os.path.splitext(self.fpath)[1].lower()
        self.ffmpeg_bin = find_binary('ffmpeg', abort=True)
        self.pydub_sound = None  # Populate with self.create_pydub_sound()

    def compress(self, output_fpath: typing.Union[None, str, pathlib.Path]=None):
        """
        Compress a local audio file by exporting it at 32K. If `output_fpath` isn't specified,
        an output file name will be automatically generated by adding the suffix "-COMPRESSED"
        to the input filepath.
        """
        if output_fpath is None:
            output_fpath = append_filename_suffix(self.fpath, '-COMPRESSED')

        cmd = f'{self.ffmpeg_bin} -i "{self.fpath}" -map 0:a:0 -b:a 32k "{output_fpath}" -y'
        out = syscmd(cmd)

        logger.info(f'Compressed audio "{self.fpath}" and created "{output_fpath}"')
        return out

    def join(self,
             additional_audio_files: typing.Union[list, str, pathlib.Path],
             output_fpath: typing.Union[None, str, pathlib.Path]=None):
        """
        Join audio file onto one or more audio files, in order.
        """
        additional_audio_files = ensurelist(additional_audio_files)

        # Use a temporary text file with the name of each input file in the call to ffmpeg
        tmp_txtfile = os.path.join(os.path.dirname(self.fpath),
                                   'audiofile_join_' + str(os.getpid()) + '.txt')

        # Make sure that filenames don't have specific characters
        replace_strings = {"'": 'SINGLEQUOTE'}

        fpath_map = {}
        with open(tmp_txtfile, 'w') as f:
            for fpath in ensurelist(self.fpath) + additional_audio_files:
                new_fpath = fpath
                for key, val in replace_strings.items():
                    new_fpath = new_fpath.replace(key, val)

                fpath_map[fpath] = new_fpath
                os.rename(fpath, new_fpath)
                f.write(f"file '{new_fpath}'\n")

        if output_fpath is None:
            output_fpath = append_filename_suffix(self.fpath, '-JOINED')

        cmd = f'{self.ffmpeg_bin} -f concat -safe 0 -i "{tmp_txtfile}" -c copy "{output_fpath}" -y'
        out = syscmd(cmd)

        # Undo renaming of `replace_strings`
        for f, nf in fpath_map.items():
            os.rename(nf, f)

        if os.path.isfile(tmp_txtfile):
            os.remove(tmp_txtfile)

        logger.info(f'Joined selected file "{self.fpath}" onto "{str(additional_audio_files)}" and created "{output_fpath}"')
        return out

    def split(self, segment_time: int):
        """
        Split audiofile into chunks of a desired length (in seconds).
        """
        cmd = '{} -i "{}" -f segment -segment_time {} -c copy "{}-ffmpeg-%03d{}" -y'.format(
            self.ffmpeg_bin,
            self.fpath,
            segment_time,
            os.path.splitext(self.fpath)[0],
            os.path.splitext(self.fpath)[1])
        out = syscmd(cmd)

        # Find output files
        dpath = os.path.dirname(self.fpath)
        dpath = '.' if dpath == '' else dpath
        os.chdir(dpath)
        splitfiles = listfiles(path=dpath,
                               pattern=r'%s-ffmpeg-\d{3}\.%s' % \
                                   (os.path.basename(os.path.splitext(self.fpath)[0]),
                                    os.path.splitext(self.fpath)[1].replace('.', '')))

        if dpath != '.':
            splitfiles = [os.path.join(dpath, x) for x in splitfiles]

        logger.info(f'Split audiofile "{self.fpath}" into chunks of size {segment_time} seconds')
        return splitfiles

    def get_duration(self):
        """
        Get the duration of a WAV audio file in seconds.
        """
        if self.ext != '.wav':
            logger.warning(f'File "{self.fpath}" is not a WAV, but this format is required to get_duration(), exporting temp WAV file')
            tmp_wav = os.path.join(os.path.dirname(self.fpath), f'get_duration_{os.getpid()}.wav')
            self.convert(output_fpath=tmp_wav, output_format='wav')
            target_fpath = tmp_wav
        else:
            target_fpath = self.fpath

        with contextlib.closing(wave.open(target_fpath, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        if self.ext != '.wav':
            if os.path.isfile(tmp_wav):
                os.remove(tmp_wav)

        logger.info(f'Detected duration of "{self.fpath}": {duration} seconds')
        return duration

    def create_audio_segment(self):
        """
        Create an audio file segment from local file. This is a necessary step for
        some methods in this class.
        """
        if self.ext == '.mp3':
            self.pydub_sound = AudioSegment.from_mp3(self.fpath)
        elif self.ext == '.wav':
            self.pydub_sound = AudioSegment.from_wav(self.fpath)
        else:
            self.pydub_sound = AudioSegment.from_file(self.fpath)

    def convert(self, output_format=['mp3', 'wav'], output_fpath=None):
        """
        Convert an audio file to destination format and write with identical filename with pydub.
        Acceptable output formats are 'mp3' and 'wav'.
        """
        if self.pydub_sound is None:
            self.create_audio_segment()

        output_format = '.' + output_format.replace('.', '').lower()  # Ensure leading period

        assert output_format in ['.mp3', '.wav']
        assert self.ext != output_format, f'Cannot convert a {self.ext} file to the same format as itself'

        # Build output filepath if not built
        if output_fpath is None:
            output_fpath = os.path.splitext(self.fpath)[0] + '-CONVERTED' + output_format

        # Execute conversion
        if self.ext == '.m4a' and output_format == '.mp3':
            cmd = f'{self.ffmpeg_bin} -i "{self.fpath}" -codec:v copy -codec:a libmp3lame -q:a 2 "{output_fpath}"'
            syscmd(cmd)
        else:
            self.pydub_sound.export(output_fpath, format=output_format.replace('.', ''))

        logger.info(f'Converted file "{output_fpath}" to format "{output_format}"')

    def set_channels(self, num_channels):
        """
        Wrapper for pydub.AudioSegment.set_channels().
        """
        self.pydub_sound = self.pydub_sound.set_channels(num_channels)


    def transcribe(self,
                   max_gcs_clip_length: typing.Union[int, float]=50):
        """
        Transcribe an audio file using Google Cloud. WAV format is required, so
        create a temporary WAV format file if self.fpath is not already in WAV format.

        Use `max_gcs_clip_length` to specify the maximum length in seconds of a clip to
        send to GCS for transcription. Typically, clips under 60 seconds will avoid
        cloud transcription issues.
        """
        def is_google_credentials_set():
            """
            Check OS environment for GOOGLE_APPLICATION_CREDENTIALS.
            """
            return 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ.keys()

        def set_google_credentials(google_app_credentials_json_fpath):
            """
            Set environment variable as path to Google credentials JSON file.
            """
            if not is_google_credentials_set():
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = google_app_credentials_json_fpath
                logger.info(f'Set google application credentials "{google_app_credentials_json_fpath}"')


        tmp_dpath = os.path.join(os.path.dirname(self.fpath), '.tmp.pydoni.transcribe')
        if os.path.isdir(tmp_dpath):
            shutil.rmtree(tmp_dpath)

        os.mkdir(tmp_dpath)
        tmp_fpath = os.path.join(tmp_dpath, 'transcribe_' + f'{os.getpid()}.wav')
        if self.ext != '.wav':
            # Export WAV format of current file to temporary directory
            self.convert(output_fpath=tmp_fpath, output_format='wav')
        else:
            # Siply copy WAV input file to temporary directory
            shutil.copyfile(self.fpath, tmp_fpath)

        audio_wav = AudioFile(tmp_fpath)

        credentials = os.path.expanduser('~/google-cloud-sdk/doni-speech-to-text-ebfb6aece133.json')
        set_google_credentials(credentials)

        # Split audio file into segments if longer than `max_gcs_clip_length` seconds
        duration = audio_wav.get_duration()

        if np.floor(duration) > max_gcs_clip_length:
            tmp_fpaths_to_transcribe = audio_wav.split(segment_time=max_gcs_clip_length)
        else:
            tmp_fpaths_to_transcribe = ensurelist(tmp_fpath)

        transcript = []
        client = speech.SpeechClient()

        for fpath in tmp_fpaths_to_transcribe:
            try:
                with open(fpath, 'rb') as audio_file:
                    content = audio_file.read()
                    audio = speech.RecognitionAudio(content=content)
                    config = speech.RecognitionConfig(
                        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                        # sample_rate_hertz=400,
                        language_code='en-US',
                        audio_channel_count=1,
                        enable_separate_recognition_per_channel=False)

                    response = client.recognize(config=config, audio=audio)

                # Each result is for a consecutive portion of the audio. Iterate through
                # them to get the transcripts for the entire audio file.
                for result in response.results:
                    # The first alternative is the most likely one for this portion.
                    transcript.append(result.alternatives[0].transcript)

            except Exception as e:
                if os.path.isdir(tmp_dpath):
                    shutil.rmtree(tmp_dpath)

                raise e


        # De-capitalize first letter of each transcript. This happens as a long audio segment is
        # broken into smaller clips, the first word in each of those clips becomes capitalized.
        transcript = [x[0].lower() + x[1:] for x in transcript]
        transcript = re.sub(r' +', ' ', ' '.join(transcript)).strip()

        if os.path.isdir(tmp_dpath):
            shutil.rmtree(tmp_dpath)

        return transcript


class AppleScript(object):
    """
    Store Applescript-wrapper operations.
    """
    def __init__(self):
        pass

    def execute(self, applescript: str):
        """
        Execute AppleScript string.
        """
        out = osascript(applescript)
        if 'error' in out.lower():
            raise Exception(str(out))

    def new_terminal_tab(self):
        """
        Make new Terminal window.
        """
        applescript = """
        tell application "Terminal"
            activate
            tell application "System Events" to keystroke "t" using command down
            repeat while contents of selected tab of window 1 starts with linefeed
                delay 0.01
            end repeat
        end tell"""

        self.execute(applescript)

    def execute_shell_script_in_new_tab(self, shell_script_str: str):
        """
        Create a new Terminal tab, then execute given shell script string.
        """
        applescript = """
        tell application "Terminal"
            activate
            tell application "System Events" to keystroke "t" using command down
            repeat while contents of selected tab of window 1 starts with linefeed
                delay 0.01
            end repeat
            do script "{}" in window 1
        end tell
        """.format({shell_script_str.replace('"', '\\"')})

        applescript = applescript.replace('\\\\"', '\"')
        self.execute(applescript)


def syscmd(cmd: typing.Union[str, list], encoding: str=''):
    """
    Runs a command on the system, waits for the command to finish, and then returns the
    text output of the command. If the command produces no text output, the command's
    return code will be returned instead. Optionally decode output bytestring.
    """
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         close_fds=True)

    p.wait()
    output = p.stdout.read()

    if len(output) > 1:
        if encoding > '' and isinstance(output, bytes):
            return output.decode(encoding)
        else:
            return output
    else:
        logger.var('output', output)
        logger.warning('Length of `output` is <=1, returning the process returncode')

        return p.returncode


def find_binary(bin_name: str,
                additional_bin_paths: list=[],
                abort: bool=False,
                return_all: bool=False):
    """
    Find system binary by name. If multiple binaries found, return the first one found unless `return_all` is True, in which case return a list of binaries found. If `abort` is True,
    then raise an error in the case that the desired binary is not found.

    Example:
        >>> find_binary('exiftool')
        # If exiftool installed
        '/usr/local/exiftool'

        # If exiftool installed in multiple locations and `return_all` is True
        ['/usr/local/exiftool', '/usr/bin/exiftool']

        # If exiftool installed in multiple locations and `return_all` is False
        /usr/local/exiftool

        # If exiftool not installed
        None
    """
    bin_paths = [x for x in sys.path if os.path.basename(x) in ['bin', 'lib']] + \
        ['/usr/bin', '/usr/local/bin']

    if len(additional_bin_paths):
        bin_paths = bin_paths + additional_bin_paths

    bin_paths = list(set(bin_paths))

    match = []
    for path in bin_paths:
        os.chdir(path)
        binaries = pydoni.listfiles()
        for binary in binaries:
            if bin_name == binary:
                match_item = os.path.join(path, binary)
                match.append(match_item)
                logger.info(f'Matching binary found "{match_item}"')

    if len(match) > 1:
        if return_all:
            logger.warning(f"Multiple matches found for '{bin_name}', returning all: '{str(match)}'")
            return match
        else:
            logger.warning(f"Multiple matches found for '{bin_name}': {str(match)}, selected first")
            return match[0]

    elif len(match) == 0:
        if abort:
            raise FileNotFoundError(f"No matching binaries found for '{bin_name}'")
        else:
            logger.warning('No matching binaries found, returning None')
        return None

    return match[0]


def is_adobe_dng_converter_installed():
    """
    Check whether Adobe DNG Converter app is installed on the local system.
    """
    return os.path.isfile('/Applications/Adobe DNG Converter.app/Contents/MacOS/Adobe DNG Converter')


def adobe_dng_converter(fpath: typing.Union[str, pathlib.Path]):
    """
    Run Adobe DNG Converter on a file.
    """
    app_path = '/Applications/Adobe DNG Converter.app/Contents/MacOS/Adobe DNG Converter'
    cmd = f'"{app_path}" "{fpath}"'
    syscmd(cmd)


def stat(fpath: typing.Union[str, pathlib.Path]):
    """
    Call 'stat' UNIX command and parse output into a Python dictionary with items:
        - File
        - Size
        - FileType
        - Mode
        - Uid
        - Device
        - Inode
        - Links
        - AccessDate
        - ModifyDate
        - ChangeDate
    """
    def parse_datestring(fpath: typing.Union[str, pathlib.Path], datestring: str):
        """
        Extract datestring from `stat` output.
        """
        try:
            dt = datetime.datetime.strptime(datestring, '%a %b %d %H:%M:%S %Y')
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logger.error(f"Unable to parse date string '{datestring}' for '{fpath}' (original date string returned)", error_msg=str(e))
            return datestring


    # Get output of `stat` command and clean for python list
    exiftool_bin = find_binary('stat')
    cmd = f'{exiftool_bin} -x "{fpath}"'
    res = syscmd(cmd, encoding='utf-8')
    res = [x.strip() for x in res.split('\n')]

    # Tease out each element of `stat` output
    items = ['File', 'Size', 'FileType', 'Mode', 'Uid', 'Device', 'Inode', 'Links',
             'AccessDate', 'ModifyDate', 'ChangeDate']

    out = {}
    for item in items:
        try:
            if item == 'File':
                out[item] = res[0].split(':')[1].split('"')[1]
            elif item == 'Size':
                out[item] = res[1].split(':')[1].strip().split(' ')[0]
            elif item == 'FileType':
                out[item] = res[1].split(':')[1].strip().split(' ')[1]
            elif item == 'Mode':
                out[item] = res[2].split(':')[1].strip().split(' ')[0]
            elif item == 'Uid':
                out[item] = res[2].split(':')[2].replace('Gid', '').strip()
            elif item == 'Device':
                out[item] = res[3].split(':')[1].replace('Inode', '').strip()
            elif item == 'Inode':
                out[item] = res[3].split(':')[2].replace('Links', '').strip()
            elif item == 'Links':
                out[item] = res[3].split(':')[3].strip()
            elif item == 'AccessDate' :
                out[item] = parse_datestring(fpath, res[4].replace('Access:', '').strip())
            elif item == 'ModifyDate' :
                out[item] = parse_datestring(fpath, res[5].replace('Modify:', '').strip())
            elif item == 'ChangeDate' :
                out[item] = parse_datestring(fpath, res[6].replace('Change:', '').strip())

        except Exception as e:
            out[item] = f'<stat() ERROR: {str(e)}>'
            logger.exception(f"Error extracting key '{item}' from stat output: {str(e)}")

    return out


def mid3v2(fpath: typing.Union[str, pathlib.Path], attr_name: str, attr_value: Any):
    """
    Use mid3v2 to add or overwrite a file metadata attribute. Acceptable attribute names:
        - artist
        - album
        - song
        - comment
        - picture
        - genre
        - year
        - date
        - track
    """
    valid_attr_names = ['artist', 'album', 'song', 'comment', 'picture', 'genre', 'year', 'date', 'track']
    assert attr_name in valid_attr_names, f"Attribute '{attr_name} is not a valid attribute: {str(valid_attr_names)}"

    mid3v2_bin = find_binary('mid3v2', abort=True)
    cmd = f'{mid3v2_bin} --{attr_name}="{attr_value}" "{fpath}"'

    return syscmd(cmd)


def convert_audible(fpath: typing.Union[str, pathlib.Path], fmt: str, activation_bytes: str):
    """
    Convert Audible .aax file to .mp4. Parameter `activation_bytes` is the activation
    bytes string. See https://github.com/inAudible-NG/audible-activator to get your
    activation byte string if you don't have one.

    Acceptable values for parameter `fmt` are 'mp3' and 'mp4'.
    """
    assert os.path.splitext(fpath)[1].lower() == '.aax', f'File "{fpath}" is not of type "aax"'

    fmt = fmt.lower().replace('.', '')
    valid_fmts = ['mp3', 'mp4']
    assert fmt in valid_fmts, f"Invalid extension '{fmt}', must be one of {str(valid_fmts)}"

    output_fpath = os.path.splitext(fpath)[0] + '.mp4'
    assert not os.path.isfile(output_fpath)

    # Convert to mp4 (regardless of `fmt` parameter)
    ffmpeg_bin = find_binary('ffmpeg')
    cmd = f'{ffmpeg_bin} -activation_bytes {activation_bytes} -i "{fpath}" -vn -c:a copy "{output_fpath}" -y'
    syscmd(cmd)

    if fmt == 'mp3':
        # Convert to mp3
        AudioFile(output_fpath).convert(output_format='mp3')


def mp4_to_mp3(fpath: typing.Union[str, pathlib.Path], bitrate: typing.Union[int, str]):
    """
    Convert an .mp4 file to a .mp3 file. Select `bitrate` as an integer to export
    the file with. May also be a string such as '192k', but must end with 'k'.
    """
    assert os.path.splitext(fpath)[1].lower() == '.mp4', 'Input file is not an mp4'
    ffmpeg_bin = find_binary('ffmpeg', abort=True)

    # Get bitrate as string ###k where ### is any number
    bitrate = str(bitrate).replace('k', '') + 'k'
    assert re.match(r'\d+k', bitrate), '`bitrate` must be an integer or a string followed by "k"'

    cmd = 'f="{}";{} -i "$f" -acodec libmp3lame -ab {} "${{f%.mp4}}.mp3" -y'.format(fpath, ffmpeg_bin, bitrate)

    return syscmd(cmd)


def split_video_scenes(fpath: typing.Union[str, pathlib.Path],
                       output_dpath: typing.Union[str, pathlib.Path]):
    """
    Split video file using PySceneDetect.
    """
    scenedetect_bin = find_binary('scenedetect', abort=True)
    cmd = f'{scenedetect_bin} --input "{fpath}" --output "{output_dpath}" detect-content split-video'
    return syscmd(cmd)


def osascript(applescript: str):
    """
    Execute AppleScript string.
    """
    osascript_bin = find_binary('osascript', abort=True)
    applescript = applescript.replace("'", "\'")

    cmd = f"{osascript_bin} -e '{applescript}'"

    return syscmd(cmd, encoding='utf-8')


def video_to_gif(video_fpath: typing.Union[str, pathlib.Path],
                 gif_fpath: typing.Union[None, str, pathlib.Path]=None,
                 fps: int=10):
    """
    Convert a video file to a .gif. Auto-generate `gif_file` if unspecified.
    """
    ffmpeg_bin = find_binary('ffmpeg', abort=True)
    video_fpath = os.path.abspath(video_fpath)

    if gif_fpath is None:
        gif_fpath = pydoni.append_filename_suffix(video_fpath, '-CONVERTED')
        gif_fpath = os.path.splitext(gif_fpath)[0] + '.gif'

    cmd = f'{ffmpeg_bin} -i "{video_fpath}" -r {str(fps)} "{gif_fpath}"'
    out = subprocess.call(cmd, shell=True)

    logger.info(f'Converted "{video_fpath}" to format "{gif_fpath}"')
    return out

# User prompting ---------------

def user_select_from_list(lst: list,
                          indent: int=0,
                          msg: str=None,
                          adjustment: int=0,
                          valid_opt: list=None,
                          allow_range: bool=True,
                          return_idx: bool=False,
                          noprint: bool=False):
    """
    Prompt user to make a selection from a list. Supports comma- and hyphen-separated selection.

    Example:
        A user may select elements from a list as:
        1-3, 5, 10-15, 29  ->  [1,2,3,5,10,11,12,13,14,15,29]

    lst {list} list of items to select from
    indent {int} indentation level of all items of `lst`
    msg {str} custom message to print instead of default
    adjustment {int} numeric adjust for enumerated display list
    valid_opt {list} list of valid options, defaults to `lst`
    allow_range {bool} allow user to make multiple selections using commas and/or hyphens
    return_idx {bool} return index of selections in `lst` instead of `lst` items
    noprint {bool} do not print `lst` to console
    """
    def get_valid_opt(lst, adjustment=1):
        """
        Build a numeric list in the format of:

            [
                0 + adjustment,
                1 + adjustment,
                2 + adjustment,
                ...
                len(lst)-1 + adjustment
            ]
        """
        valid_opt = []

        for i, item in enumerate(lst):
            valid_opt.append(i + adjustment)

        return valid_opt

    def print_lst(lst, indent, adjustment=1):
        """
        Print an enumerated list to console.
        """
        tab = '  ' * indent
        for i, item in enumerate(lst):
            print(f'{tab}({str(i + adjustment)}) {item}')

    def define_msg(msg, allow_range):
        """
        Build a message string to print along with the printed list.
        """
        if msg is None:
            if allow_range is True:
                msg = 'Please make a selection (hyphen-separated range ok)'
            else:
                msg = 'Please make a single selection'

        return msg

    def parse_numeric_input(uin_raw, valid_opt, allow_range, silent=False):
        """
        Parse user numeric input to list. If allow_range is False, then input
        must be a single digit. If not, then user may enter input with hyphen(s)
        and comma(s) to indicate different slices of a list.

        Example:
            From a list of [0, 1, 2, 3, 4, 5] a user might enter
            '0-2,4', which should be translated as [0, 1, 2, 4].
            This function will then return [0, 1, 2, 4].

        uin_raw {str} user raw character input
        allow_range {bool} allow_range parent funtion flag
        silent {bool} suppress error messages and just return False if invalid entry entered
        """
        def error_func(msg):
            """
            Print string on invalid input, but do not raise an error.
            """
            echo(msg, error=True)

        # Test that input is valid mix of digits, hyphens and commas only
        if not re.match(r'^(\d|-|,)+$', uin_raw):
            if not silent:
                echo('Input must consist of digits, hyphens and/or commas only', error=True)

            return False

        if allow_range:
            uin_raw = uin_raw.split(',')
            out = []

            for x in uin_raw:
                if '-' in x:

                    start = x.split('-')[0]
                    if start.strip().isdigit():
                        start = int(start)
                    else:
                        if not silent:
                            echo(f"'Start' component '{start}' of hyphen-separated range unable to be parsed", error=True)

                        return False

                    stop = x.split('-')[1]
                    if stop.strip().isdigit():
                        stop = int(stop) + 1
                    else:
                        if not silent:
                            echo(f"'Stop' component '{stop}' of hyphen-separated range unable to be parsed", error=True)

                        return False

                    if start >= stop:
                        if not silent:
                            echo(f"Invalid range '{x}'. 'Start' must be >= 'stop'", error=True)

                        return False

                    out.append(list(range(start, stop)))

                elif x.strip().isdigit():
                    out.append([int(x)])

                else:
                    if not silent:
                        echo(f"Component '{str(x)}' could not in valid format", error=True)

                    return False

            out = list(set([item for sublist in out for item in sublist]))

            oos = []
            for x in out:
                if x not in valid_opt:
                    oos.append(x)

            if len(oos):
                if not silent:
                    error_func(f"Value{'s' if len(oos) > 1 else ''} {str(oos)} out of valid range {str(valid_opt)}")

                return False

            return out

        else:
            if uin_raw.strip().isdigit():
                return [int(uin_raw)]
            else:
                return False

    if not noprint:
        print_lst(lst, indent, adjustment)

    valid_opt = get_valid_opt(lst, adjustment) if not valid_opt else valid_opt
    msg = define_msg(msg, allow_range)

    sel = False
    while sel is False:
        uin_raw = get_input(msg)
        sel = parse_numeric_input(uin_raw, valid_opt, allow_range)

    if return_idx:
        return sel[0] if len(sel) == 1 else sel
    else:
        out = [x for i, x in enumerate(lst) if i + adjustment in sel]
        return out[0] if len(out) == 1 else out


def user_select_from_list_inq(lst: list, msg: str='Select an option'):
    """
    Use PyInquirer module to prompt user to select an item or items from a list.
    """
    style = inq.style_from_dict({
        inq.Token.QuestionMark: '#E91E63 bold',
        inq.Token.Selected: '#673AB7 bold',
        inq.Token.Instruction: '',
        inq.Token.Answer: '#2196f3 bold',
        inq.Token.Question: '',
    })

    question = [{
        'type': 'list',
        'name': 'option',
        'message': msg,
        'choices': lst,
    }]

    selection = inq.prompt(question)['option']

    return selection


def get_input(msg: str='Enter input', mode: str='str', indicate_mode: bool=False):
    """
    Get user input, optionally of specified format.

    msg {str} message to print to console
    mode {str} apply filter to user input, one of ['bool', 'date', 'int', 'float',
               'str', 'file', 'filev', 'dir', 'dirv']. 'filev' and 'dirv'
               options are {exists}'file'/'dir' with an added layer of validation, to
    indicate_mode {bool} print type of anticipated datatype with message
    """
    assert mode in ['str', 'bool', 'date', 'int', 'float', 'file', 'filev', 'dir', 'dirv']

    add_colon = lambda x: x + ': '
    add_clarification = lambda x, clar: x + ' ' + clar

    # Add suffix based on `mode`
    msg = re.sub(r': *$', '', msg).strip()
    if mode == 'bool':
        msg = add_clarification(msg, '(y/n)')
    elif mode == 'date':
        msg = add_clarification(msg, '(YYYY-MM-DD)')
    if indicate_mode:
        msg = add_clarification(msg, '{%s}' % mode)
    msg = add_colon(msg)

    uin_raw = input(msg)

    if mode == 'bool':
        while not test_value(uin_raw, 'bool'):
            uin_raw = input("Must enter 'y' or 'n': ")
        if uin_raw.lower() in ['y', 'yes']:
            return True
        else:
            return False
    elif mode == 'date':
        while not test_value(uin_raw, 'date') and uin_raw != '':
            uin_raw = input("Must enter valid date in format 'YYYY-MM-DD': ")
    elif mode == 'int':
        while not test_value(uin_raw, 'int'):
            uin_raw = input('Must enter integer value: ')
        uin_raw = int(uin_raw)
    elif mode == 'float':
        while not test_value(uin_raw, 'float'):
            uin_raw = input('Must enter float value: ')
    elif mode in ['file', 'filev', 'dir', 'dirv']:
        uin_raw = os.path.expanduser(uin_raw.strip())
        if mode == 'filev':
            while not os.path.isfile(uin_raw):
                uin_raw = input('Must enter existing file: ')
        elif mode == 'dirv':
            while not os.path.isdir(uin_raw):
                uin_raw = input('Must enter existing directory: ')

    return uin_raw


def get_input_inq(msg: str='Enter input', mode: str='str', indicate_mode: bool=False):
    """
    Get user input for single line using PyInquirer module.

    msg {str} message to print to console
    mode {str} apply filter to user input, one of ['bool', 'date', 'int', 'float',
               'str', 'file', 'filev', 'dir', 'dirv']. 'filev' and 'dirv' options
               are 'file {str}/'dir' with an added layer of validation, to ensure the file/dir exists
    indicate_mode {bool} print type of anticipated datatype with message
    """
    assert mode in ['str', 'bool', 'date', 'int', 'float', 'file', 'filev', 'dir', 'dirv']

    def define_validator(mode):
        """
        Define 'InqValidator' class based on 'mode'.

            mode {str}'mode' parameter passed into parent

        """

        testfunc = lambda value: test_value(value, mode)

        class InqValidator(inq.Validator):
            def validate(self, document):
                if not testfunc(document.text):
                    raise inq.ValidationError(
                        message="Please enter a valid value of type '%s'" % mode,
                        cursor_position=len(document.text))

        return InqValidator

    add_colon = lambda x: x + ': '
    add_clarification = lambda x, clar: x + ' ' + clar

    # Add suffix based on `mode`
    msg = re.sub(r': *$', '', msg).strip()
    if mode == 'bool':
        msg = add_clarification(msg, '(y/n)')
    elif mode == 'date':
        msg = add_clarification(msg, '(YYYY-MM-DD)')
    if indicate_mode:
        msg = add_clarification(msg, '{%s}' % mode)

    msg = add_colon(msg)

    question = {
        'type': 'input',
        'name': 'TMP',
        'message': msg
    }

    if mode in ['bool', 'date', 'int', 'float', 'file', 'filev', 'dir', 'dirv']:
        validator = define_validator(mode)
        question['validate'] = validator

    question = [question]
    answer = inq.prompt(question)['TMP']

    if mode == 'int':
        answer = int(answer)
    elif mode == 'float':
        answer = float(answer)
    elif mode == 'bool':
        if answer.lower() in ['y', 'yes', 'true', 't']:
            answer = True
        elif answer.lower() in ['n', 'no', 'false', 'f']:
            answer = False
    elif mode in ['file', 'filev', 'dir', 'dirv']:
        answer = os.path.expanduser(answer)

    return answer


def continuous_prompt(msg: str, mode='str', indicate_mode: bool=False, use_inq: bool=False):
    """
    Continuously prompt the user for input until '' is entered.

    msg {str} message to print to console
    mode {str} apply filter to user input, one of ['bool', 'date', 'int', 'float',
               'str', 'file', 'filev', 'dir', 'dirv']. 'filev' and 'dirv'
               options are {exists}'file'/'dir' with an added layer of validation, to
    indicate_mode {bool} print type of anticipated datatype with message
    use_inq {bool} use `get_input_inq()` instead of `get_input()`
    """
    uin = 'TMP'
    all_input = []

    while uin > '':
        if use_inq:
            uin = get_input_inq(msg=msg, mode=mode, indicate_mode=indicate_mode)
        else:
            uin = get_input(msg=msg, mode=mode, indicate_mode=indicate_mode)

        if uin > '':
            all_input.append(uin)

    return all_input

# Database operations ---------------

class Postgres(object):
    """
    Interact with PostgreSQL database through Python.
    """
    def __init__(self,
                 hostname: str=None,
                 port: str=None,
                 db_name: str=None,
                 pg_user: str=None,
                 pw: str=None,
                 credentials_fpath: str=os.path.expanduser('~/.pgpass')) -> None:
        # Get credentials
        credentials_fpath = os.path.expanduser(credentials_fpath)
        if os.path.isfile(credentials_fpath):
            self.hostname, self.port, self.db_name, self.pg_user, self.pw = self.read_pgpass(credentials_fpath)
        else:
            self.hostname = hostname
            self.port = port
            self.db_name = db_name
            self.pg_user = pg_user
            self.pw = pw

        assert self.hostname is not None, 'Must provide hostname'
        assert self.port is not None, 'Must provide port'
        assert self.db_name is not None, 'Must provide database name'
        assert self.pg_user is not None, 'Must provide username'
        assert self.pw is not None, 'Must provide password'

        self.dbcon = self.connect()

        self.null_equivalents = ['nan', 'n/a', 'null', 'none', '']
        self.null_equivalents = self.null_equivalents + [x.upper() for x in self.null_equivalents]

    def read_pgpass(self, credentials_fpath: str) -> tuple:
        """
        Read ~/.pgpass file if it exists and extract Postgres credentials. Return tuple
        in format: `hostname, port, db_name, user_name, password`
        """
        with open(os.path.expanduser(credentials_fpath), 'r') as f:
            pgpass_contents = f.read().split(':')

        # Ensure proper pgpass format, should be a tuple of length 5
        assert len(pgpass_contents) == 5, \
            'Invalid ~/.pgpass contents format. Should be `hostname:port:db_name:user_name:password`'

        return tuple(pgpass_contents)

    def connect(self):
        """
        Connect to Postgres database and return the database connection.
        """
        con_str = f'postgresql://{self.pg_user}@{self.hostname}:{self.port}/{self.db_name}'
        return sqlalchemy.create_engine(con_str)

    def execute(self,
                sql: str,
                logfile: typing.Union[str, pathlib.Path]=None,
                log_ts: bool=False,
                progress: bool=False) -> None:
        """
        Execute a SQL string or a list of SQL statements.
        """
        write_log = False if logfile is None else True
        if write_log:
            logger.info(f'Writing SQL query log to file "{logfile}"')

        sql = ensurelist(sql)

        with self.dbcon.begin() as con:
            if progress:
                pbar = tqdm(total=len(sql), unit='query')

            for stmt in sql:
                con.execute(sqlalchemy.text(stmt))

                if write_log:
                    with open(logfile, 'a') as f:
                        entry = stmt + '\n'

                        if log_ts:
                            entry = systime(as_string=True) + ' ' + entry

                        f.write(entry)

                if progress:
                    pbar.update(1)

        if progress:
            pbar.close()

    def read_sql(self, sql: str, simplify: bool=True) -> typing.Union[pd.Series, pd.DataFrame]:
        """
        Execute SQL and read results using Pandas, optionally simplify result to a Series if
        the result is a single-column dataframe.
        """
        res = pd.read_sql(sql, con=self.dbcon)

        if res.shape[1] == 1:
            if simplify:
                logger.info(f'Simplifying result data to pd.Series, length: {str(len(res))}')
                res = res.iloc[:, 0]

        return res

    def get_table_name(self, schema_name: str=None, table_name: str=None) -> str:
        """
        Concatenate a schema and table names. Require that `table_name` is supplied,
        but `schema_name` may be blank (i.e. in the case of querying pg_stat, or another
        builtin table that does not have an explicit corresponding schema.)
        """
        assert table_name is not None, 'Must supply `table_name`'

        if schema_name is None:
            return table_name
        else:
            return schema_name + '.' + table_name

    def validate_dtype(self, schema_name: str, table_name: str, col: str, val: Any) -> bool:
        """
        Query database for datatype of value and validate that the Python value to
        insert to that column is compatible with the SQL datatype.
        """
        if table_name.startswith('pg_'):
            # Builtin table housed in `pg_catalog` schema, but no schema required to query from it
            schema_name = 'pg_catalog'

        table_schema_and_name = self.get_table_name(schema_name, table_name)
        full_col = table_schema_and_name + '.' + col

        infoschema = self.infoschema(infoschema_table='columns')[['table_schema', 'table_name', 'column_name', 'data_type', 'is_nullable']]
        infoschema = infoschema.loc[
            (infoschema['table_schema']==schema_name)
            & (infoschema['table_name']==table_name)
            & (infoschema['column_name']==col)
        ]

        assert len(infoschema), f'Nonexistent column {full_col}'
        infoschema = infoschema.squeeze().to_dict()

        if val == 'NULL' or val is None:
            if bool(infoschema['is_nullable']) is True:
                return True
            else:
                logger.error(f"Value 'NULL' (dtype: {val.__class__.__name__}) not allowed for column {full_col}")
                return False

        # Check that input value datatype matches queried table column datatype
        dtype = self.col_dtypes(schema_name, table_name)[col]
        dtype_map = {
            'bigint': 'int',
            'int8': 'int',
            'bigserial': 'int',
            'serial8': 'int',
            'integer': 'int',
            'int': 'int',
            'int4': 'int',
            'smallint': 'int',
            'int2': 'int',
            'double precision': 'float',
            'float': 'float',
            'float4': 'float',
            'float8': 'float',
            'numeric': 'float',
            'decimal': 'float',
            'character': 'str',
            'char': 'str',
            'character varying': 'str',
            'varchar': 'str',
            'text': 'str',
            'date': 'str',
            'timestamp': 'str',
            'timestamp with time zone': 'str',
            'timestamp without time zone': 'str',
            'name': 'str',
            'boolean': 'bool',
            'bool': 'bool',
        }

        # Get python equivalent of SQL column datatype according to dtype_map above
        python_dtype = [v for k, v in dtype_map.items() if dtype in k]

        if not len(python_dtype):
            known_python_datatypes = list(set([v for k, v in dtype_map.items()]))
            logger.error(advanced_strip(f"""
            Unable to match SQL column '{full_col}' datatype {dtype} to any known Python
            datatypes {known_python_datatypes}"""))
            return False
        else:
            python_dtype = python_dtype[0]

        true_python_dtype = type(val).__name__

        # Prepare message to be used in event of incompatible datatypes
        msg = f"""Incompatible datatypes! SQL column {full_col} has type
        `{dtype}`, and Python value `{str(val)}` is of type `{val.__class__.__name__}`."""

        # Begin validation
        if true_python_dtype in ['date', 'datetime']:
            if 'date' in dtype or 'timestamp' in dtype:
                return True
            else:
                return False

        elif python_dtype == 'bool':
            if isinstance(val, bool):
                return True
            else:
                if isinstance(val, str):
                    if val.lower() in ['t', 'true', 'f', 'false']:
                        return True

        elif python_dtype == 'int':
            if isinstance(val, int):
                return True
            else:
                if isinstance(val, str):
                    try:
                        int(val)
                        return True
                    except:
                        pass

        elif python_dtype == 'float':
            if isinstance(val, float):
                return True
            else:
                if val == 'inf':
                    pass
                try:
                    float(val)
                    return True
                except:
                    pass

        elif python_dtype == 'str':
            if isinstance(val, str):
                return True
        else:
            return True

        # If this function hasn't returned True by now, then datatype validation must have failed
        logger.debug(msg)
        return False

    def infoschema(self, infoschema_table: str) -> pd.DataFrame:
        """
        Query from information_schema. Vanilla call to this function executes:

            select * from information_schema.{columns_or_tables};

        Can also set `infoschema_table` to "tables", or any other subdivision of Postgres'
        information schema.
        """
        sql = f'select *\nfrom information_schema.{infoschema_table}'
        df = self.read_sql(sql, simplify=False)
        logger.info(f'Retrieved information_schema.{infoschema_table}')

        # Format known column datatypes
        bool_cols = ['is_nullable']
        for bcol in bool_cols:
            if bcol in df.columns:
                df[bcol] = df[bcol].map(lambda x: dict(YES=True, NO=False)[x])

        return df

    def build_update(self,
                     schema_name,
                     table_name,
                     pkey_name,
                     pkey_value,
                     columns,
                     values,
                     validate=True,
                     newlines=False) -> str:
        """
        Construct a SQL UPDATE statement.

        By default, this method will:

            - Attempt to coerce a date value to proper format if the input value is detect_dtype
              as a date but possibly in the improper format. Ex: '2019:02:08' -> '2019-02-08'
            - Quote all values passed in as strings. This will include string values that
              are coercible to numerics. Ex: '5', '7.5'.
            - Do not quote all values passed in as integer or boolean values.
            - Primary key value is quoted if passed in as a string. Otherwise, not quoted.

        schema {str} name of schema
        table {str} SQL table name
        pkey_name {str} name of primary key in table
        pkey_value {str} value of primary key for value to update
        columns {list} columns to consider in UPDATE statement
        values {list} values to consider in UPDATE statement
        validate {bool} validate that each value may be inserted to destination column
        newlines {true} add newlines to query string to make more human-readable
        """
        columns = ensurelist(columns)
        values = ensurelist(values)
        if len(columns) != len(values):
            raise Exception("Parameters `columns` and `values` must be of equal length")

        pkey_value = self._single_quote(pkey_value)
        lst = []

        for col, val in zip(columns, values):
            if validate:
                test = self.validate_dtype(schema_name, table_name, col, val)
                if not test:
                    dtype = type(val).__name__
                    raise Exception(f'Dtype mismatch. Value: {val}, dtype: {dtype}, column: {col}')

            if str(val).lower() in self.null_equivalents:
                val = 'NULL'
            elif test_value(val, 'bool') or test_value(val, 'int') or test_value(val, 'float'):
                pass
            else:
                # Assume string
                val = self._single_quote(val)

            if newlines:
                lst.append(f'\n    "{col}"={str(val)}')
            else:
                lst.append(f'"{col}"={str(val)}')

        sql = ["UPDATE {}", "SET {}", "WHERE {} = {}"]
        if newlines:
            lst[0] = lst[0].strip()
            sql = '\n'.join(sql)
        else:
            sql = ' '.join(sql)

        table_schema_and_name = self.get_table_name(schema_name, table_name)
        return sql.format(table_schema_and_name,
                          ', '.join(lst),
                          '"' + pkey_name + '"',
                          pkey_value)

    def build_insert(self,
                     schema_name: str,
                     table_name: str,
                     columns: list,
                     values: list,
                     validate: bool=False,
                     newlines: bool=False) -> str:
        """
        Construct SQL INSERT statement.
        By default, this method will:

            - Attempt to coerce a date value to proper format if the input value is
              detect_dtype as a date but possibly in the improper format.
              Ex: '2019:02:08' -> '2019-02-08'
            - Quote all values passed in as strings. This will include string values
              that are coercible to numerics. Ex: '5', '7.5'.
            - Do not quote all values passed in as integer or boolean values.
            - Primary key value is quoted if passed in as a string. Otherwise, not quoted.

        schema {str} name of schema
        table {str} SQL table name
        columns {list} columns to consider in UPDATE statement
        values {list} values to consider in UPDATE statement
        validate {bool} validate that each value may be inserted to destination column
        newlines {true} add newlines to query string to make more human-readable
        """
        columns = ensurelist(columns)
        values = ensurelist(values)
        if len(columns) != len(values):
            raise Exception("Parameters `columns` and `values` must be of equal length")

        lst = []
        for col, val in zip(columns, values):
            if validate:
                test = self.validate_dtype(schema_name, table_name, col, val)
                if not test:
                    dtype = type(val).__name__
                    raise Exception(advanced_strip(f"""Value '{val}' (dtype: {dtype})
                    is incompatible with column '{col}' """))

            if str(val).lower() in self.null_equivalents:
                val = 'null'

            elif test_value(val, 'bool') or test_value(val, 'int') or test_value(val, 'float'):
                pass
            else:
                # Assume string, handle quotes
                val = self._single_quote(val)

            lst.append(val)

        values_final = ', '.join(str(x) for x in lst)
        values_final = values_final.replace("'null'", 'null')
        columns = ', '.join(['"' + x + '"' for x in columns])

        table_schema_and_name = self.get_table_name(schema_name, table_name)
        sql = ['insert into {table_schema_and_name} ({columns})', 'values ({values_final})']
        sql = '\n'.join(sql) if newlines else ' '.join(sql)

        return sql.format(**locals())

    def build_delete(self,
                     schema_name: str,
                     table_name: str,
                     pkey_name: str,
                     pkey_value: Any,
                     newlines: bool=False) -> str:
        """
        Construct SQL DELETE FROM statement.
        """
        table_schema_and_name = self.get_table_name(schema_name, table_name)

        if isinstance(pkey_value, list):
            pkey_value_lst = [self._single_quote(x) for x in pkey_value]
            sql = ['delete from {}', 'where {} in ({})']
            pkey_value_str = ', '.join([str(x) for x in pkey_value_lst])
        else:
            pkey_value_str = self._single_quote(pkey_value)
            sql = ['delete from {}', 'where {} = {}']

        sql = '\n'.join(sql) if newlines else ' '.join(sql)
        return sql.format(table_schema_and_name, pkey_name, pkey_value_str)

    def col_names(self, schema_name: str, table_name: str) -> list:
        """
        Get column names of table as a list.
        """
        df_cols = self.infoschema(infoschema_table='columns')[['table_schema', 'table_name', 'column_name']]

        df_cols = df_cols.loc[(df_cols['table_schema'] == schema_name)
                              & (df_cols['table_name'] == table_name)]

        cols = df_cols['column_name'].tolist()
        return cols

    def col_dtypes(self, schema_name: str, table_name: str) -> list:
        """
        Get column datatypes of table as a dictionary.
        """
        infoschema = self.infoschema(infoschema_table='columns')
        infoschema = infoschema.loc[
            (infoschema['table_schema']==schema_name)
            & (infoschema['table_name']==table_name)
        ]
        return infoschema.set_index('column_name')['data_type'].to_dict()

    def read_table(self, schema_name: str, table_name: str) -> pd.DataFrame:
        """
        Read an entire SQL table or view as a dataframe.
        """
        df = self.read_sql(f'select * from "{schema_name}"."{table_name}"')
        logger.info(f"Read dataframe {schema_name}.{table_name}, shape: {df.shape}")
        return df

    def dump(self, backup_dir: typing.Union[str, pathlib.Path])-> str:
        """
        Wrap `pg_dump` and save an entire database contents to a directory.
        """
        backup_dir = os.path.expanduser(backup_dir)
        logger.info(f'Dumping database {self.db_name} to "{backup_dir}"')

        bin = find_binary('pg_dump', abort=True)
        output_fpath = f'{backup_dir}/{self.db_name}.sql'
        cmd = f'{bin} --user {self.pg_user} {self.db_name} > "{output_fpath}"'

        out = syscmd(cmd, encoding='utf-8')
        if not isinstance(out, int):
            if 'FATAL' in out:
                raise Exception(out.strip())

        return output_fpath

    def dump_tables(self, backup_dir: typing.Union[str, pathlib.Path], sep: str=',', coerce_csv: bool=False):
        """
        Dump each table in database to a textfile with specified separator.

        Source: https://stackoverflow.com/questions/17463299/export-database-into-csv-file?answertab=oldest#tab-top
        """
        db_to_csv = """
        CREATE OR REPLACE FUNCTION db_to_csv(path TEXT) RETURNS void AS $$
        DECLARE
           tables RECORD;
           statement TEXT;
        BEGIN
        FOR tables IN
           SELECT (table_schema || '.' || table_name) AS schema_table
           FROM information_schema.tables t
               INNER JOIN information_schema.schemata s ON s.schema_name = t.table_schema
           WHERE t.table_schema NOT IN ('pg_catalog', 'information_schema')
               AND t.table_type NOT IN ('VIEW')
           ORDER BY schema_table
        LOOP
           statement := 'COPY ' || tables.schema_table || ' TO ''' || path || '/' || tables.schema_table || '.tmpcsv' ||''' DELIMITER ''{sep}'' CSV HEADER';
           EXECUTE statement;
        END LOOP;
        RETURN;
        END;
        $$ LANGUAGE plpgsql;""".format(**locals())
        self.execute(db_to_csv)

        # Execute function, dumping each table to a textfile.
        # Function is used as follows: SELECT db_to_csv('/path/to/dump/destination');
        logger.info(f'Dumping database {self.db_name} to "{backup_dir}" as tables stored as textfiles')
        self.execute(f"select db_to_csv('{backup_dir}')")

        # If coerce_csv is True, read in each file outputted, then write as a quoted CSV.
        # Replace 'sep' if different from ',' and quote each text field.
        if coerce_csv:
            if sep != ',':
                owd = os.getcwd()
                os.chdir(backup_dir)

                # Get tables that were dumped and build filenames
                get_dumped_tables = """
                select (table_schema || '.' || table_name) as schema_table
                from information_schema.tables t
                join information_schema.schemata s
                  on s.schema_name = t.table_schema
                where t.table_schema not in ('pg_catalog', 'information_schema')
                  and t.table_type not in ('VIEW')
                order by schema_table"""
                dumped_tables = self.read_sql(get_dumped_tables).squeeze()

                if isinstance(dumped_tables, pd.Series):
                    dumped_tables = dumped_tables.tolist()
                elif isinstance(dumped_tables, str):
                    dumped_tables = [dumped_tables]

                dumped_tables = [x + '.csv' for x in dumped_tables]

                # Read in each table and overwrite file with comma sep and quoted text values
                for csvfile in dumped_tables:
                    pd.read_csv(csvfile, sep=sep).to_csv(
                        csvfile, quoting=csv.QUOTE_NONNUMERIC, index=False)

                os.chdir(owd)
            else:
                logger.warning('`coerce_csv` is True but desired `sep` is not a comma!')

        # Get tables that were just dumped and return their filenames
        dumped_files_tmpcsv = listfiles(path=backup_dir, ext='tmpcsv', full_names=True)
        dumped_files = []
        for tmpcsvfile in dumped_files_tmpcsv:
            newfilename = os.path.splitext(tmpcsvfile)[0] + '.csv'
            os.rename(tmpcsvfile, newfilename)
            dumped_files.append(newfilename)

        return dumped_files

    def create_schema(self, schema_name: str) -> None:
        """
        Create a Postgres schema.
        """
        self.execute(f'create schema {schema_name}')

    def drop_schema(self, schema_name: str, if_exists: bool=False, cascade: bool=False) -> None:
        """
        Drop a Postgres schema with options to only drop if it currently exists, and
        to drop dependent objects on it with `cascade`.
        """
        cascade_str = ' cascade' if cascade else ''
        if_exists_str = 'if exists ' if if_exists else ''
        self.execute(f'drop schema {if_exists_str}{schema_name}{cascade_str}')

    def drop_schema_and_recreate(self, schema_name: str, if_exists: bool=False, cascade: bool=False) -> None:
        """
        Drop then re-create a Postgres schema
        """
        args = dict(table_scham=schema_name, if_exists=if_exists, cascade=cascade)
        self.drop_schema(**args)
        self.create_schema(schema_name)

    def drop_schema_if_exists_and_recreate(self, schema_name: str, cascade: bool=False) -> None:
        """
        Drop then re-create a Postgres schema
        """
        self.drop_schema_if_exists(schema_name, cascade=cascade)
        self.create_schema(schema_name)

    def list_tables(self, schema_name: str=None) -> pd.DataFrame:
        """
        Query information schema for a list of tables present in the database connection.
        """
        additional_cond = f"and table_schema = '{schema_name}'" if isinstance(schema_name, str) else ''
        sql = f"""
        select table_schema, "table_name"
        from information_schema.tables
        where table_type = 'BASE TABLE'
          {additional_cond}
        """
        return self.read_sql(sql)

    def table_exists(self, schema_name: str=None, table_name: str=None) -> bool:
        """
        Return a boolean indicating whether a table is existent in the database connection
        """
        tables = self.list_tables(schema_name)
        return table_name in tables['table_name'].tolist()

    def create_table(self, schema_name: str, table_name: str, columnspec: dict, if_not_exists: bool=False):
        """
        Create a Postgres table given a schema name, table name and column specification. The
        specification must be in format:

            {
                col1_name:col1_dtype,
                col2_name:col2_dtype,
                ...
            }
        """
        tab_ws = '    '

        columnspec_lst = []
        for col, dtype in columnspec.items():
            line_item = col + ' ' + dtype + ',\n'
            columnspec_lst.append(line_item)

        columnspec_str = tab_ws + tab_ws.join(columnspec_lst).rstrip('\n,')

        if_not_exists_str = 'if not exists ' if if_not_exists else ''
        create_table_sql_lst = [
            f'create table {if_not_exists_str}{schema_name}.{table_name} (',
            columnspec_str,
            ')',
        ]

        create_table_sql = '\n'.join(create_table_sql_lst)
        self.execute(create_table_sql)

    def wipe_table(self, schema_name: str, table_name: str) -> None:
        """
        Delete all records in a table but do not drop the table.
        """
        if self.table_exists(schema_name, table_name):
            self.execute(f'delete from {schema_name}.{table_name} where 1 = 1')

    def drop_table(self, schema_name: str, table_name: str, if_exists: bool=False, cascade: bool=False) -> None:
        """
        Drop a Postgres table.
        """
        if_exists_str = 'if exists ' if if_exists else ''
        cascade_str = ' cascade' if cascade else ''
        sql = f'drop table {if_exists_str}"{schema_name}"."{table_name}"{cascade_str}'
        self.execute(sql)

    def list_views(self, schema_name: str=None) -> pd.DataFrame:
        """
        Query information schema for a list of views present in the database connection.
        """
        where_clause = f"where table_schema = '{schema_name}'" if isinstance(schema_name, str) else ''
        sql = f"""
        select table_schema as view_schema, "table_name" as view_name
        from information_schema.views
        {where_clause}
        order by table_schema, view_name
        """
        return self.read_sql(sql)

    def view_exists(self, schema_name: str=None, view_name: str=None) -> bool:
        """
        Return a boolean indicating whether a view is existent in the database connection
        """
        views = self.list_views(schema_name)
        return view_name in views['view_name'].tolist()

    def table_or_view_exists(self, schema_name: str=None, table_or_view_name: str=None) -> bool:
        """
        Determine whether a table or view exists in the database connection.
        """
        return self.table_exists(schema_name, table_or_view_name) or self.view_exists(schema_name, table_or_view_name)

    def create_view(self, schema_name: str, view_name: str, view_sql: str, or_replace: bool=False):
        """
        Create a view from user-passed SQL.
        """
        or_replace_str = 'or replace ' if or_replace else ''
        sql = f'create {or_replace_str}view "{schema_name}"."{view_name}" as ({view_sql})'
        self.execute(sql)

    def drop_view(self, schema_name: str, view_name: str, if_exists: bool=False, cascade: bool=False) -> None:
        """
        Drop a Postgres view.
        """
        if_exists_str = 'if exists ' if if_exists else ''
        cascade_str = ' cascade' if cascade else ''
        sql = f'drop view {if_exists_str}"{schema_name}"."{view_name}"{cascade_str}'
        self.execute(sql)

    def trigger_exists(self, trigger_schema: str=None, trigger_name: str=None) -> bool:
        """
        Return a boolean indicating whether a trigger is existent in the database connection
        """
        triggers = self.list_triggers(trigger_schema)
        return trigger_name in triggers['trigger_name'].tolist()

    def list_triggers(self, trigger_schema: str=None) -> list:
        """
        Query information schema for a list of triggers present in the database connection.
        """
        where_clause = f"where trigger_schema = '{trigger_schema}'" if isinstance(trigger_schema, str) else ''
        sql = f"""
        select event_object_schema as table_schema
               , event_object_table as "table_name"
               , trigger_schema
               , trigger_name
               , string_agg(event_manipulation, ',') as "event"
               , action_timing as activation
               , action_condition as "condition"
               , action_statement as definition
        from information_schema.triggers
        {where_clause}
        group by 1, 2, 3, 4, 6, 7, 8
        order by table_schema, "table_name"
        """
        return self.read_sql(sql)

    def _single_quote(self, val: Any):
        """
        Escape single quotes and put single quotes around value if string value.
        """
        if type(val) not in [bool, int, float]:
            val = str(val).replace("'", "''")
            val = "'" + val + "'"

        return val


# Web tools ---------------

def check_network_connection(abort: bool=False) -> bool:
    """
    Check if connected to internet.
    """
    is_network_connected = test_url('https://www.google.com', quiet=True)

    error_msg = 'No network connection!'
    if is_network_connected:
        return True
    else:
        if abort:
            raise Exception(error_msg)
        else:
            logger.error('No network connection!')
            return False


def test_url(url: str, quiet: bool=False):
    """
    Test if a url is available using the requests library.
    """
    try:
        requests.get(url)
        return True
    except Exception as e:
        if not quiet:
            logger.exception(e)
            logger.error(f'URL {url} not available')

        return False


def get_element_by_selector(url: str, selector: str, attr_name: str=None):
    """
    Extract HTML text by CSS selector from a target URL. Optionally extract an attribute
    specified by `attr_name` from the element selected via `selector`.
    """
    # import html

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    if attr_name:
        return [soup.select(selector)[i].attrs[attr_name] for i in range(len(soup.select(selector)))]

    elem = [soup.select(selector)[i].text for i in range(len(soup.select(selector)))]
    return elem


def get_element_by_xpath(url: str, xpath: str):
    """
    Extract HTML text by xpath selector from a target URL.
    """
    page = requests.get(url)
    tree = lxml_html.fromstring(page.content)
    return tree.xpath(xpath)


def downloadfile(url: str, destfile: bool=None, method: str='requests'):
    """
    Download file from the web to a local file. `method` can be one of 'requests' or 'curl'.
    """
    assert method in ['requests', 'curl']

    if method == 'requests':
        assert isinstance(destfile, str)

        r = requests.get(url, stream=True)
        with open(destfile, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

    elif method == 'curl':
        if isinstance(destfile, str):
            cmd = f'curl -o "{destfile}" "{url}"'
        else:
            cmd = 'curl -O "{url}"'

        syscmd(cmd)


def is_good_response(resp: requests.models.Response):
    """
    Returns True if the GET response seems to be HTML, False otherwise.
    """
    resp_obj = resp.thing if hasattr(resp, 'thing') else resp
    content_type = resp_obj.headers['Content-Type'].lower()
    return (resp_obj.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def simple_get(url: str):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with contextlib.closing(requests.get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        logger.error(f'Error during requests to {url} : {str(e)}')
        return None


# Image operations ---------------

def make_meme(img_fpath: typing.Union[str, pathlib.Path],
              output_fpath: typing.Union[str, pathlib.Path],
              msg: str,
              msg_color: str='white',
              msg_pos: str='bottom',
              msg_outline_color: str='black',
              msg_outline_width: int=3,
              font_path: typing.Union[str, pathlib.Path]='/System/Library/Fonts/HelveticaNeue.ttc',
              font_size: int=200,
              repel_from_edge: float=0.0):
    """
    Draw text on an image file.

    img_fpath {str} image file to draw on
    output_fpath {str} filepath to save output image to
    msg {str} message to write on image
    msg_color {str} color of message
    msg_pos {str} position of message, only 'bottom' supported
    msg_outline_color {str} message outline color
    msg_outline_width {int} width of text outline
    font_path {str} path to font to use, alternative '/Library/Fonts/Arial Black.ttf'
    font_size {int} desired font size of `msg`
    repel_from_edge: shift text position this % of the image
        height/width away from the edge if text position is an edge of
        the image. Example: if the specified position is top-left, the text
        will be printed right up against the top and left edges. If a value
        of 0.05 is specified for `repel_from_edge`, then the text will be
        shifted down 5% of the image height and shifted right 5% of the
        image {float}width
    """
    img = Image.open(img_fpath)
    draw = ImageDraw.Draw(img)

    lines = []

    font = ImageFont.truetype(font_path, font_size)
    w, h = draw.textsize(msg, font)

    img_width_w_padding = img.width * 0.99

    # 1. How many lines for the msg to fit ?
    line_count = 1
    if w > img_width_w_padding:
        line_count = int(round((w / img_width_w_padding) + 1))

    if line_count > 2:
        while 1:
            font_size -= 2
            font = ImageFont.truetype(font_path, font_size)
            w, h = draw.textsize(msg, font)
            line_count = int(round((w / img_width_w_padding) + 1))
            if line_count < 3 or font_size < 10:
                break

    # If msg contains no spaces but is long enough to justify multiple
    # lines, revert to line_count = 1 as the next part will fail, attempting
    # to split the message into multiple lines on a space
    if line_count > 1 and ' ' not in msg:
        line_count = 1

    # 2. Divide text in X lines
    last_cut = 0
    isLast = False
    for i in range(0,line_count):
        if last_cut == 0:
            cut = (len(msg) / line_count) * i
        else:
            cut = last_cut

        if i < line_count-1:
            next_cut = (len(msg) / line_count) * (i+1)
        else:
            next_cut = len(msg)
            isLast = True

        # Make sure we don't cut words in half
        next_cut = int(next_cut)
        next_cut_original = next_cut
        if next_cut == len(msg) or msg[next_cut] == " ":
            pass
        else:
            # Check forward and backward from next_cut to get position of
            # string to cut at (look for nearest whitespace)
            while msg[next_cut] != " ":
                if next_cut == len(msg)-1:
                    next_cut = next_cut_original
                    break
                next_cut += 1

            while msg[next_cut] != " ":
                next_cut -= 1

        cut = int(cut)
        line = msg[cut:next_cut].strip()

        # Is line still fitting?
        w, h = draw.textsize(line, font)
        if not isLast and w > img_width_w_padding:
            next_cut -= 1
            while msg[next_cut] != " ":
                next_cut -= 1

        last_cut = next_cut
        lines.append(msg[cut:next_cut].strip())

    last_y = -h
    if msg_pos == 'bottom':
        repel_pixels = repel_from_edge * img.height
        repel_pixels = int(repel_pixels)
        last_y = img.height - h * (line_count+1) - repel_pixels

    for i in range(0, line_count):
        w, h = draw.textsize(lines[i], font)
        test_x = img.width/2 - w/2
        test_y = last_y + h

        mow = msg_outline_width
        moc = msg_outline_color
        if moc is not None:
            draw.text((test_x-mow, test_y-mow), lines[i], moc, font=font)
            draw.text((test_x+mow, test_y-mow), lines[i], moc, font=font)
            draw.text((test_x+mow, test_y+mow), lines[i], moc, font=font)
            draw.text((test_x-mow, test_y+mow), lines[i], moc, font=font)

        draw.text((test_x, test_y), lines[i], msg_color, font=font)
        last_y = test_y

    img.save(output_fpath)


def ocr_image(image_fpath: typing.Union[str, pathlib.Path], preprocess: bool=None):
    """
    Apply PyTesseract OCR to an image file.

    Source:
        https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/

    Optionally pre-process an image with the `preprocess` parameter. Acceptable
    values are 'thresh' or 'anti_blur',
    """
    # Load the example image and convert it to grayscale
    image = cv2.imread(image_fpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Check to see if we should apply thresholding to preprocess the image
    if isinstance(preprocess, str):
        if preprocess == 'thresh':
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            logger.info('Thresholding applied in image preprocessing')

        # Make a check to see if median blurring should be done to remove noise
        elif preprocess == 'anti_blur':
            gray = cv2.medianBlur(gray, 3)
            logger.info('Anti-blurring applied in image preprocessing')

        else:
            raise Exception(f'Valid `preprocess` parameter items are "thresh" and "blur"')

    # Write the grayscale image to disk as a temporary file so we can apply OCR to it
    tmpfile = os.path.join(os.path.dirname(image_fpath),
                           'image_ocr_' + str(os.getpid()) + os.path.splitext(image_fpath)[1])
    cv2.imwrite(tmpfile, gray)

    # Load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
    text = pytesseract.image_to_string(Image.open(tmpfile))
    logger.info(f'PyTesseract OCR complete of file "{image_fpath}"')

    if os.path.isfile(tmpfile):
        os.remove(tmpfile)

    return text


def get_blur_value(image_fpath):
    """
    Detect the Laplacian blur value of an image file.

    Source:
        https://pysource.com/2019/09/03/detect-when-an-image-is-blurry-opencv-with-python/
    """
    img = cv2.imread(image_fpath)
    laplacian = cv2.Laplacian(img, cv2.CV_64F)
    return laplacian.var()


# Backend module operations ---------------

def what_is_my_name(classname=None, with_modname=True):
    """
    Return name of function that calls this function. If called from a
    classmethod, include classname before classmethod in output string. Use
    parameter `with_modname` to toggle whether to append module name to
    beginning of function name.
    """
    lst = []
    funcname = inspect.stack()[1][3]

    if with_modname:
        modulename = inspect.getmodule(inspect.stack()[1][0]).__name__
        if modulename != '__main__':
            lst += [modulename]

    if isinstance(classname, str):
        lst += [classname]

    lst += [funcname]
    return '.'.join(lst)


def __pydonicli_register__(var_dict):
    """
    Register variable as a part of the 'pydoni' module to be logged to the CLI's backend.
    """
    for key, value in var_dict.items():
        setattr(pydoni, 'pydonicli_' + key, value)


def __pydonicli_declare_args__(var_dict):
    """
    Limit a dictionary, usually `locals()` to exclude modules and functions and thus contain
    only key:value pairs of variables.
    """
    vars_only = {}

    for k, v in var_dict.items():
        dtype = v.__class__.__name__
        if dtype not in ['module', 'function']:
            vars_only[k] = v

    return vars_only
