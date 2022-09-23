"""Command line"""
import click
from click import Context

from python_project import __version__
from python_project.config import settings
from python_project.log import init_log


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    '-V',
    '--version',
    is_flag=True,
    help='Show version and exit.'
)  # If it's true, it will override `settings.VERBOSE`
@click.option('-v', '--verbose', is_flag=True, help='Show more info.')
@click.option(
    '--debug',
    is_flag=True,
    help='Enable debug.'
)  # If it's true, it will override `settings.DEBUG`
def main(ctx: Context, version: str, verbose: bool, debug: bool):
    """Main commands"""
    if version:
        click.echo(__version__)
    elif ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
    else:
        if verbose:
            settings.set('VERBOSE', True)
        if debug:
            settings.set('DEBUG', True)


@main.command()
def run():
    """Run command"""
    init_log()
    click.echo('run......')

import argparse
import sys

from python_project.counter import count


def init_args() -> argparse.Namespace:
    """Init argument and parse"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', required=True, help='Source file used for count.')
    parser.add_argument('-d', '--dest', required=True, help='Dest file used for count result')
    return parser.parse_args(sys.argv[1:])


def main():
    """Execute"""
    args = init_args()
    count(args.source, args.dest)


if __name__ == '__main__':
    main()