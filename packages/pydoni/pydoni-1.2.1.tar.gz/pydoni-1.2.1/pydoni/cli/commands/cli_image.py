import click
import pydoni
from .common import Verbose
from os.path import splitext


@click.option('-f', '--fpath', type=click.Path(exists=True), required=True, multiple=True,
              help='Path to audiofile(s) to compress.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')
@click.command()
def ocr(fpath, verbose):
    """
    OCR an image using pytesseract.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    vb = Verbose(verbose)

    fpaths = list(fpath)
    for fpath in fpaths:
        vb.info(f'Applying OCR to file "{fpath}"...')
        text = pydoni.ocr_image(fpath)

        with open(splitext(fpath)[0] + '.txt', 'w') as f:
            f.write(text)

        vb.info("Successfully OCR'd file")

    result['ocr_files'] = fpaths
    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='image.ocr'))


@click.group(name='image')
def cli_image():
    """Doni image-based CLI tools."""
    pass


cli_image.add_command(ocr)
