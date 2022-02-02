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


def _get_store(store_url, creds_file=None):
    return JASMINObjectStore(store_url, creds_file=creds_file)


def _get_store_url(ctx, param, value):

    if not value:
        print("FROM ENV VAR")
        value = "Set from env"

    if not value.startswith("http"):
        raise ClickException(f"Store URL must start with: 'http'. You provided: {value}")

    return value


def _get_credentials(ctx, param, creds_file=None):
    if creds_file and not os.path.isfile(creds_file):
        raise ClickException(f"Credentials file does not exist: '{creds_file}'")
        # else:
        #     try:
        #         creds = json.load(open(creds_file))
        #     except:
        #         raise ClickException(f"Cannot read credentials from: {creds_file}")

    return creds_file


@click.group()
def main():
    """Console script for jos."""
    click.echo("You are running the 'jos' command-line.")
    return 0


@main.command()
@click.argument("bucket_id")
@click.option("-s", "--store-url", callback=_get_store_url)
@click.option("-c", "--creds-file", callback=_get_credentials)
def create_bucket(bucket_id, store_url, creds_file):
    #params = ctx.params
    #click.echo(f"create with buck id {bucket_id}!, {store_url}, {creds_file}")
    j = _get_store(store_url, creds_file)
    j.create_bucket(bucket_id)


def _show_listing(contents, key):
    if not contents:
        click.echo(f"No {key}s found.")
    else:
        click.echo(f"{len(contents)} {key}s found:")
        for item in contents:
            click.echo(f"\t{item}")


@main.command()
@click.option("--details/--no-details", default=False)
@click.option("-s", "--store-url", callback=_get_store_url)
@click.option("-c", "--creds-file", callback=_get_credentials)
def list_buckets(details, store_url, creds_file):
    j = _get_store(store_url, creds_file)
    contents = j.list_buckets(details=details)
    _show_listing(contents, key="bucket")


@main.command()
@click.argument("bucket_id")
@click.option("--details/--no-details", default=False)
@click.option("-s", "--store-url", callback=_get_store_url)
@click.option("-c", "--creds-file", callback=_get_credentials)
def list_bucket(bucket_id, details, store_url, creds_file):
    j = _get_store(store_url, creds_file)
    contents = j.list_bucket(bucket_id, details=details)
    _show_listing(contents, key="object")


@main.command()
@click.argument("file_path")
@click.option("-b", "--bucket-id")
@click.option("-s", "--store-url", callback=_get_store_url)
@click.option("-c", "--creds-file", callback=_get_credentials)
def put(file_path, bucket_id, store_url, creds_file):
    j = _get_store(store_url, creds_file)
    j.put_file(bucket_id, file_path)


@main.command()
@click.argument("file_id")
@click.option("-b", "--bucket-id")
@click.option("-t", "--target-dir")
@click.option("-s", "--store-url", callback=_get_store_url)
@click.option("-c", "--creds-file", callback=_get_credentials)
def get(file_id, bucket_id, target_dir, store_url, creds_file):
    j = _get_store(store_url, creds_file)
    j.get_file(bucket_id, file_id, target_dir)


@main.command()
@click.argument("bucket_id")
@click.option("-s", "--store-url", callback=_get_store_url)
@click.option("-c", "--creds-file", callback=_get_credentials)
def delete_bucket(bucket_id, store_url, creds_file):
    j = _get_store(store_url, creds_file)
    j.delete_bucket(bucket_id)


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
