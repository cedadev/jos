import os
import time
import click

from jos import JASMINObjectStore


jos = None
STORE_URL = "http://name-o.s3.jc.rl.ac.uk/"
BUCKET_ID = "test-bucket"
CREDS_FILE = f"{os.path.expanduser('~')}/.credentials/jos-name-manager.json"
TEST_FILE = "test_file.dat"
BUCKET_FILE_PATH = BUCKET_ID + "/" + TEST_FILE
SIZE = os.path.getsize(TEST_FILE)


def _OLDsetup_module():
    global jos
    jos = JASMINObjectStore(STORE_URL, creds_file=CREDS_FILE)

    # Clear up old test stuff, if exists
    if jos._fs.exists(BUCKET_ID):
        jos.delete_bucket(BUCKET_ID)
        time.sleep(2)

"jos create bucket_id --creds-file|-c --store-url|-u"
def test_create_bucket():
    jos.create_bucket(BUCKET_ID)

"jos put filepath bucket_id  --creds-file|-c --store-url|-u"
def test_put_file():
    jos.put_file(BUCKET_ID, TEST_FILE)
    time.sleep(1)

"jos list bucket|path --detail|-d  --creds-file|-c --store-url|-u"  # Same as below?
def test_list_buckets():
    # Simple list
    buckets = jos.list_buckets()
    assert BUCKET_ID in buckets

    # Details list
    records = jos.list_buckets(detail=True)
    assert BUCKET_ID in [item["Key"] for item in records]
    assert "BUCKET" in [item["StorageClass"] for item in records]

"jos list bucket|path --detail|-d  --creds-file|-c --store-url|-u"
def test_list_bucket():
    # Simple list
    buckets = jos.list_bucket(BUCKET_ID)
    assert BUCKET_FILE_PATH in buckets

    # Details list
    records = jos.list_bucket(BUCKET_ID, detail=True)
    assert BUCKET_FILE_PATH in [item["Key"] for item in records]
    assert SIZE in [item["size"] for item in records]

"jos get bucket/filepath targetdir  --creds-file|-c --store-url|-u"
def test_get_file(tmp_path):
    target_dir = tmp_path / "testdir"
    tmpfile = target_dir / TEST_FILE

    jos.get_file(BUCKET_ID, TEST_FILE, target_dir.as_posix())

    assert tmpfile.exists()
    assert open(tmpfile.as_posix()).read() == open(TEST_FILE).read()

def test_get_files():
    pass

"jos delete bucket_id  --creds-file|-c --store-url|-u"
def test_delete_bucket():
    if jos._fs.exists(BUCKET_ID):
        jos.delete_bucket(BUCKET_ID)
