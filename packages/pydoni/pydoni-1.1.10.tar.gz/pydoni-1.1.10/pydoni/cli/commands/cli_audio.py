import click
import pydoni
from .common import Verbose
from gtts import gTTS
from os import stat
from os.path import splitext, isfile, join, expanduser


@click.option('-f', '--fpath', type=click.Path(exists=True), required=True, multiple=True,
              help='Path to audiofile(s) to compress.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to STDOUT.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')
@click.command()
def compress(fpath, verbose, notify):
    """
    Compress one or more audiofiles.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    vb = Verbose(verbose)

    fpaths = list(fpath)
    for fpath in fpaths:
        ffmpeg_output = pydoni.AudioFile(fpath).compress()
        vb.info(f'Successfully compressed file "{fpath}"')

    if notify:
        pydoni.macos_notify(title='M4A to MP3 Conversion Complete!')

    result['compressed_files'] = fpaths
    result['ffmpeg_output'] = ffmpeg_output

    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='audio.compress'))


@click.option('-f', '--fpath', type=click.Path(exists=True), required=True, multiple=True,
              help='Path to audiofiles to concatenate.')
@click.option('-o', '--output-fpath', type=click.Path(), required=False, default=None,
              help='Desired path to output audiofile.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to STDOUT.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')
@click.command()
def join_files(fpath, output_fpath, verbose, notify):
    """
    Concatenate multiple audio files with FFmpeg.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    assert len(fpath) > 1, 'Must pass more than one file to join!'
    vb = Verbose(verbose)

    fpaths = list(fpath)
    vb.info(f'Joining {len(fpaths)-1} additional audio files onto base file "{fpaths[0]}"...')

    if output_fpath is None:
        output_fpath = pydoni.append_filename_suffix(fpaths[0], '-JOINED')

    audio = pydoni.AudioFile(audio_fpath=fpaths[0])
    ffmpeg_output = audio.join(additional_audio_files=fpaths[1:], output_fpath=output_fpath)
    vb.info(f'Output audiofile created "{output_fpath}"')

    if notify:
        pydoni.macos_notify(title='Audiofile Join Complete!')

    outfile_size_in_bytes = stat(output_fpath).st_size
    result = dict(joined_files=fpaths,
                  output_fpath=output_fpath,
                  outfile_size_in_bytes=outfile_size_in_bytes,
                  ffmpeg_output=ffmpeg_output)

    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='audio.join_files'))


@click.option('-f', '--fpath', type=click.Path(exists=True), required=True, multiple=True,
              help='Path to audio file to convert to MP3.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to STDOUT.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')
@click.command()
def to_mp3(fpath, verbose, notify):
    """
    Convert an audio file to .mp3 format.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    vb = Verbose(verbose)
    fpaths = list(fpath)

    output_fpaths = []
    for f in fpaths:
        vb.info(f'Converting file "{f}" to MP3')
        audio = pydoni.AudioFile(f)
        output_fpath = output_fpath = splitext(f)[0] + '-CONVERTED.mp3'
        audio.convert(output_format='mp3', output_fpath=output_fpath)
        vb.info(f'Outputted .mp3 file "{output_fpath}"')
        output_fpaths.append(output_fpath)

    if notify:
        pydoni.macos_notify(message='Audiofile compression complete', title='Pydoni-CLI')

    result = {'fpaths': fpaths, 'output_fpaths': output_fpaths}
    result = dict(fpaths=fpaths)

    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='audio.to_mp3'))


@click.option('-i', '--input', type=str, multiple=True,
               help='String of text or path to input text file.')
@click.option('-o', '--output-fpath', type=click.Path(), required=False, multiple=True, default=None,
              help=pydoni.advanced_strip("""Desired path to output mp3 file(s). Must
              be either the same length as `input`, or None. If None, same file
              basename is used for each item in `input` if passed a list of files.
              If passed a list of strings, then auto-generate the output file
              for each input string."""))
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to STDOUT.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')
@click.command()
def text_to_speech(input, output_fpath, verbose, notify):
    """
    Convert raw text, either as commandline input or file input, to speech using gTTS.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    vb = Verbose(verbose)

    input = list(input)
    output = list(output_fpath)

    assert len(input), 'Must pass --input'
    assert len(output), 'Must pass --output'

    if output[0] is None:
        output = [None] * len(input)

    assert len(input) == len(output), '--input and --output-fpath must be of the same length'

    for i, o in zip(input, output):
        if isfile(i):
            # Input is file
            assert splitext(i)[1].lower() == '.txt', f'Input file "{i}" must have extension ".txt"'
            with open(i, 'r') as f:
                text_to_speechify = f.read()

            if o is None:
                # Default output file is the same as the input file but with .mp3 extension
                o = splitext(i)[0] + '.mp3'
        else:
            # Input is text
            text_to_speechify = i
            if o is None:
                # Default output file is a generic file on desktop
                o = join(expanduser('~'), 'Desktop', f'text_to_speech_{pydoni.systime(as_string=True)}.mp3')


        speech = gTTS(text=text_to_speechify, lang='en', slow=False)
        speech.save(o)

    if notify:
        pydoni.macos_notify(message='Text to speech complete', title='Pydoni-CLI')

    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='audio.text_to_sp'))


@click.group(name='audio')
def cli_audio():
    """Doni audio-based CLI tools."""
    pass

cli_audio.add_command(compress)
cli_audio.add_command(join_files)
cli_audio.add_command(to_mp3)
cli_audio.add_command(text_to_speech)
