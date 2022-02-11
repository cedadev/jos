import os
import json

from minio import Minio
from minio.deleteobjects import DeleteObject

this_dir = os.path.dirname(os.path.abspath(__file__))
STORE_URL = "name-o.s3.jc.rl.ac.uk:80"
BUCKET_ID = "test-bucket-minio"
TEST_FILE_NAME = "test_file.dat"
TEST_FILE_PATH = os.path.join(this_dir, TEST_FILE_NAME)
BUCKET_FILE_PATH = BUCKET_ID + "/" + TEST_FILE_NAME
SIZE = os.path.getsize(TEST_FILE_PATH)
CREDS_FILE = os.path.join(os.environ["HOME"], ".credentials/jos-credentials.json")

creds = json.load(open(CREDS_FILE)) 

# Create client with access and secret key.
secret = creds["secret"]
token = creds["token"]

m = Minio(STORE_URL, token, secret, secure=False)

# Create bucket.
m.make_bucket(BUCKET_ID)

# List buckets
buckets = m.list_buckets()
for bucket in buckets:
    print(bucket.name, bucket.creation_date)

# Put object
m.put_object(BUCKET_ID, TEST_FILE_NAME, open(TEST_FILE_PATH, "rb"), length=SIZE)

# List objects
objects = m.list_objects(BUCKET_ID)
for obj in objects:
    print(obj)

TMP_FILE = "newfile.dat"
resp = m.get_object(BUCKET_ID, TEST_FILE_NAME)
with open(TMP_FILE, "wb") as w:
    w.write(resp.read())

assert open(TMP_FILE).read() == open(TEST_FILE_PATH).read()

# Remove a prefix recursively.
def delete_bucket(BUCKET_ID):
    delete_object_list = map(lambda x: DeleteObject(x.object_name),
        m.list_objects(BUCKET_ID, "", recursive=True))
    errors = m.remove_objects(BUCKET_ID, delete_object_list)
    for error in errors:
        print("error occured when deleting object", error)

    m.remove_bucket(BUCKET_ID)

if m.bucket_exists(BUCKET_ID):
    delete_bucket(BUCKET_ID)


