import click
import os
import pydoni
from .common import Verbose


@click.option('-f', '--fpath', type=click.Path(exists=True), required=True, multiple=True,
              help='Video file(s) to convert to GIF.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print program messages to STDOUT.')
@click.option('-n', '--notify', is_flag=True, default=False,
              help='Fire macOS notification on program completion.')
@click.command()
def to_gif(fpath, verbose, notify):
    """
    Convert video file(s) to GIF.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    vb = Verbose(verbose)
    fpaths = list(fpath)

    for f in fpaths:
        gif_fpath = os.path.splitext(f)[0] + '.gif'
        pydoni.video_to_gif(video_fpath=f, gif_fpath=gif_fpath, fps=10)
        vb.echo(f'Outputted .gif file "{gif_fpath}"')
        result[f] = gif_fpath

    if notify:
        pydoni.macos_notify(message='Conversion complete', title='Video to GIF')

    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='video.to_gif'))


@click.group(name='video')
def cli_video():
    """Doni video-based CLI tools."""
    pass


cli_video.add_command(to_gif)
