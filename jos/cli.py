"""Console script for jos."""

__author__ = """Ag Stephens"""
__contact__ = 'ag.stephens@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import sys
import os
import json
import click
from click import ClickException

from jos import JASMINObjectStore, DEFAULT_CREDENTIALS_FILE


@click.group()
def main():
    """Console script for jos."""
    click.echo("Replace this message by putting your code into "
               "jos.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0

def get_store_url(ctx, param, value):

    if not value:
        print("FROM ENV VAR")
        value = "Set from env"

    if not value.startswith("http"):
        raise ClickException(f"Store URL must start with: 'http'. You provided: {value}")

    return value


def get_credentials(ctx, param, creds_file=None):
    if creds_file and creds_file != "auto" and not os.path.isfile(creds_file):
        raise ClickException(f"Credentials file does not exist: {creds_file}")
        # else:
        #     try:
        #         creds = json.load(open(creds_file))
        #     except:
        #         raise ClickException(f"Cannot read credentials from: {creds_file}")

    return DEFAULT_CREDENTIALS_FILE


@main.command()
#@click.option('--count', default=1, help='number of greetings')
@click.argument("bucket_id")
@click.option("-s", "--store-url", callback=get_store_url)
@click.option("-c", "--creds-file", callback=get_credentials)
@click.pass_context
def create(ctx, bucket_id, store_url, creds_file):
    #click.echo(str(get_common(ctx)))
    click.echo(str(ctx.params))
    click.echo(f"create with buck id {bucket_id}!")

@main.command()
#@click.option('--count', default=1, help='number of greetings')
@click.argument("bucket_id")
def create_bucket(bucket_id):
    click.echo(f"create with buck id {bucket_id}!")
    # global j
    # j = JASMINObjectStore(STORE_URL, creds_file=CREDS_FILE)

    # # Clear up old test stuff, if exists
    # if j._fs.exists(BUCKET_ID):
    #     j.delete_bucket(BUCKET_ID)
    #     time.sleep(2)




@main.command()
def dropdb():
    click.echo('Dropped the database')


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
