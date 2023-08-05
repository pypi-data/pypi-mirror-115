from os import remove, write
import click
import pydoni
from .common import Verbose
from os.path import expanduser, join, basename


@click.option('-d', '--dpath', type=click.Path(exists=True), required=True, multiple=True,
              help='Full path to target directory.')
@click.option('-o', '--output-fpath', type=click.Path(), default=None,
              help='If specified, write program output to this file.')
@click.option('-q', '--quiet', is_flag=True, default=False,
              help='Do not print output to console.')
@click.option('-r', '--recursive', is_flag=True, default=False,
              help='Scan recursively and iterate down the directory tree.')
@click.option('-h', '--human-readable', is_flag=True, default=False,
              help='Display filesize in output in human-readable format')
@click.option('-p', '--progress', is_flag=True, default=False,
              help='Display progress bar while scanning directory')
@click.command()
def du_by_filetype(dpath, output_fpath, recursive, quiet, human_readable, progress):
    """
    List the total filesize in a directory by file type.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    dpaths = list(dpath)
    write_lst = []

    for d in dpaths:
        write_lst.append(f'Directory "{d}"')
        filesize_dct = pydoni.du_by_filetype(dpath=d,
                                             recursive=recursive,
                                             human_readable=human_readable,
                                             progress=progress)

        for ftype, fsize in filesize_dct.items():
            write_lst.append(f'{ftype}: {fsize}')

    # Print to console
    if not quiet:
        for item in write_lst:
            print(item)

    # Write output file
    write_output = True if output_fpath is not None else False
    if write_output:
        with open(output_fpath, 'a') as f:
            for item in write_lst:
                f.write(item + '\n')

    result['result'] = filesize_dct
    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='opsys.du_by_filetype'))


@click.option('-r', '--root', type=click.Path(exists=True), required=True, multiple=True,
              help='Top-level directory to scan.')
@click.option('--recursive', is_flag=True, default=False,
              help='Scan `root` recursively and iterate down the directory tree.')
@click.option('--true-remove', is_flag=True, default=False,
              help='Delete directories that contain only empty directories.')
@click.option('--count-hidden-files/--no-count-hidden-files', is_flag=True, default=True,
              help='Count hidden files in evaluating whether directory is empty.')
@click.option('-v', '--verbose', is_flag=True, default=False,
              help='Print messages to console.')
@click.command()
def remove_empty_subfolders(root, recursive, true_remove, count_hidden_files, verbose):
    """
    Scan a directory and delete any empty bottom-level directories.
    """
    args, result = pydoni.__pydonicli_declare_args__(locals()), dict()

    dpath = list(root)
    vb = Verbose(verbose)

    removed_dirs = []
    for root in dpath:
        pydoni.remove_empty_subfolders(root=root,
                                       recursive=recursive,
                                       true_remove=true_remove,
                                       count_hidden_files=count_hidden_files)
        removed_dirs += root

    if verbose:
        if len(removed_dirs):
            for dir in removed_dirs:
                vb.info('Removed: ' + dir)
        else:
            vb.info('No empty directories found', level='warn')

    result['removed_dirs'] = removed_dirs
    pydoni.__pydonicli_register__(dict(args=args, result=result, command_name='opsys.remove_empty_subfolders'))


@click.group(name='opsys')
def cli_opsys():
    """CLI tools based on operating system actions."""
    pass


cli_opsys.add_command(remove_empty_subfolders)
cli_opsys.add_command(du_by_filetype)
