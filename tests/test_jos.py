import os
import time

from jos import JASMINObjectStore


this_dir = os.path.dirname(os.path.abspath(__file__))
j = None
CREDS_FILE = "/home/users/astephen/.credentials/jos-credentials.json"
STORE_URL = "http://name-o.s3.jc.rl.ac.uk/"
BUCKET_ID = "test-bucket-jos"
TEST_FILE_NAME = "test_file.dat"
TEST_FILE_PATH = os.path.join(this_dir, TEST_FILE_NAME)
BUCKET_FILE_PATH = BUCKET_ID + "/" + TEST_FILE_NAME
SIZE = os.path.getsize(TEST_FILE_PATH)


def setup_module():
    global j
    j = JASMINObjectStore(STORE_URL, creds_file=CREDS_FILE)

    # Clear up old test stuff, if exists
    if j._fs.exists(BUCKET_ID):
        j.delete_bucket(BUCKET_ID)
        time.sleep(2)

def teardown_module():
    if j._fs.exists(BUCKET_ID):
        j.delete_bucket(BUCKET_ID)

def test_create_bucket():
    j.create_bucket(BUCKET_ID)

def test_put_file():
    j.put_file(BUCKET_ID, TEST_FILE_PATH)
    time.sleep(1)

def test_list_buckets():
    # Simple list
    buckets = j.list_buckets()
    assert BUCKET_ID in buckets

    # Details list
    records = j.list_buckets(details=True)
    assert BUCKET_ID in [item["Key"] for item in records]
    assert "BUCKET" in [item["StorageClass"] for item in records]

def test_list_bucket():
    # Simple list
    buckets = j.list_bucket(BUCKET_ID)
    assert BUCKET_FILE_PATH in buckets

    # Details list
    records = j.list_bucket(BUCKET_ID, details=True)
    assert BUCKET_FILE_PATH in [item["Key"] for item in records]
    assert SIZE in [item["size"] for item in records]

def test_get_file(tmp_path):
    target_dir = tmp_path / "testdir"
    tmpfile = target_dir / TEST_FILE_NAME

    j.get_file(BUCKET_ID, TEST_FILE_NAME, target_dir.as_posix())

    assert tmpfile.exists()
    assert open(tmpfile.as_posix()).read() == open(TEST_FILE_PATH).read()

def test_get_files():
    # Not yet implemented
    pass

def test_delete_bucket():
    if j._fs.exists(BUCKET_ID):
        j.delete_bucket(BUCKET_ID)

