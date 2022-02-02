"""Tests for `jos` package."""

__author__ = """Ag Stephens"""
__contact__ = 'ag.stephens@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

import os
import pytest
import time

from click.testing import CliRunner
from jos import cli, JASMINObjectStore

from .test_jos import STORE_URL, TEST_FILE_NAME, TEST_FILE_PATH, SIZE

this_dir = os.path.dirname(os.path.abspath(__file__))
j = None
BUCKET_ID = "test-bucket-cli"
BUCKET_FILE_PATH = BUCKET_ID + "/" + TEST_FILE_NAME


def setup_module():
    global j
    j = JASMINObjectStore(STORE_URL)

    # Clear up old test stuff, if exists
    if j._fs.exists(BUCKET_ID):
        j.delete_bucket(BUCKET_ID)
        time.sleep(2)

def teardown_module():
    if j._fs.exists(BUCKET_ID):
        j.delete_bucket(BUCKET_ID)


def test_cli_main():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Usage: main [OPTIONS]' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

def test_cli_create_bucket():
    """Test the CLI."""
    runner = CliRunner()

    # Run: create-bucket
    result = runner.invoke(cli.main, ["create-bucket", "-s", STORE_URL, BUCKET_ID])
    assert result.exit_code == 0
    time.sleep(1)
    assert BUCKET_ID in j.list_buckets()

def test_cli_list_buckets():
    runner = CliRunner()

    # Run: list-buckets
    result = runner.invoke(cli.main, ["list-buckets", "-s", STORE_URL])
    assert result.exit_code == 0
    assert BUCKET_ID in result.output

def test_cli_list_bucket():
    runner = CliRunner()

    # Run: list-bucket (empty)
    result = runner.invoke(cli.main, ["list-bucket", "-s", STORE_URL, BUCKET_ID])
    assert result.exit_code == 0
    assert "No objects found" in result.output

def test_cli_put():
    runner = CliRunner()

    # Run: put
    result = runner.invoke(cli.main, ["put", "-s", STORE_URL, "-b", BUCKET_ID, TEST_FILE_PATH])
    assert result.exit_code == 0
    time.sleep(1)
    assert BUCKET_FILE_PATH in j.list_bucket(BUCKET_ID)

def test_cli_list_bucket_after_put():
    runner = CliRunner()

    # Run: list-bucket
    result = runner.invoke(cli.main, ["list-bucket", "-s", STORE_URL, BUCKET_ID])
    assert result.exit_code == 0
    assert TEST_FILE_NAME in result.output


def test_cli_get_bucket_after_put(tmp_path):
    runner = CliRunner()

    # Run: get
    target_dir = tmp_path / "testdir"
    tmpfile = target_dir / TEST_FILE_NAME
    result = runner.invoke(cli.main, 
                ["get", "-s", STORE_URL, "-b", BUCKET_ID, "-t", target_dir.as_posix(), TEST_FILE_NAME])

    assert result.exit_code == 0
    assert tmpfile.exists()
    assert open(tmpfile.as_posix()).read() == open(TEST_FILE_PATH).read()


def test_cli_delete_bucket():
    runner = CliRunner()

    # Run: delete-bucket
    result = runner.invoke(cli.main, ["delete-bucket", "-s", STORE_URL, BUCKET_ID])
    assert result.exit_code == 0
    time.sleep(1)
    assert BUCKET_ID not in j.list_buckets()