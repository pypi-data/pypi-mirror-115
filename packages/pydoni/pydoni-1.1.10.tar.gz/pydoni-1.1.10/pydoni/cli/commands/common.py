import click
import pydoni
import re
import time
from datetime import datetime
from emoji import emojize
from tqdm import tqdm


class Verbose(object):
    """
    Handle verbose printing to console for pydoni-cli commands. Has advantage of accepting
    a 'verbose' parameter, then not printing if that is False, similar to logging behavior.
    """
    def __init__(self, verbose=False, debug=False, timestamp=True):
        self.verbose = verbose
        self.debug_flag = debug
        self.timestamp = timestamp
        self.pbar = None

    def echo(self, *args, **kwargs):
        if self.verbose:
            kwargs['timestamp'] = self.timestamp
            echo(*args, **kwargs)

    def debug(self, *args, **kwargs):
        if self.debug_flag:
            kwargs['timestamp'] = self.timestamp
            kwargs['level'] = 'debug'
            echo(*args, **kwargs)

    def info(self, *args, **kwargs):
        if self.verbose:
            kwargs['timestamp'] = self.timestamp
            kwargs['level'] = 'info'
            echo(*args, **kwargs)

    def warn(self, *args, **kwargs):
        if self.verbose:
            kwargs['timestamp'] = self.timestamp
            kwargs['level'] = 'warn'
            echo(*args, **kwargs)

    def error(self, *args, **kwargs):
        if self.verbose:
            kwargs['timestamp'] = self.timestamp
            kwargs['level'] = 'error'
            echo(*args, **kwargs)

    def line_break(self):
        if self.verbose:
            print()

    def program_complete(self, msg='Program complete', emoji_string=':rocket:', start_ts=None):
        if self.verbose:
            emoji_string = ':' + emoji_string.replace(':', '') + ':'
            emoji_string = emojize(emoji_string, use_aliases=True)

            if start_ts is not None:
                end_ts = time.time()
                timediff = pydoni.fmt_seconds(end_ts - start_ts, units='auto', round_digits=2)
                elapsed_time = f"{timediff['value']} {timediff['units']}"
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

    def pbar_write(self, msg, refer_debug):
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


def echo(msg: str,
         level: str='info',
         arrow: str=None,
         indent: int=0,
         timestamp: bool=False,
         bold: bool=False,
         tag=None):
    """
    Pydoni-CLI echo function to print messages to console.
    """
    msg = re.sub(r'\s+', ' ', msg.strip())

    if bold:
        msg = click.style(msg, bold=True)

    letter_map = dict(debug='D', d='D', info='I', i='I', warn='W', w='W', error='E', e='E')
    letter = letter_map[level.lower()]

    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' ' if timestamp else ''
    prefix = f'[{ts}{letter}]'

    color_map = dict(D='white', I='green', W='yellow', E='red')
    prefix_colorized = click.style(prefix, fg=color_map[letter])

    arrow_str = click.style('==> ', fg=arrow, bold=True) if arrow else ''

    # `tag` must be a `ColorTag()` object
    tag_str = ''
    if tag is not None:
        if len(tag.stack):
            for x, y in tag.stack.items():
                tag_str += click.style('<' + x + '>', fg=y, bold=True) + ' '

    tag_str = tag_str.strip()
    tag_str = tag_str + ' ' if len(tag_str) else tag_str

    indent_str = '  ' * indent

    msg = str(msg)
    print("{prefix_colorized}{indent_str} {arrow_str}{tag_str}{msg}".format(**locals()))
