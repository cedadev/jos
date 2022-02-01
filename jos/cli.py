"""Console script for jos."""

__author__ = """Ag Stephens"""
__contact__ = 'ag.stephens@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
import sys
import click


@click.command()
def main(args=None):
    """Console script for jos."""
    click.echo("Replace this message by putting your code into "
               "jos.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
