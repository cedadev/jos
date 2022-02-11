## Installation

Simple installation using a virtual environment (`venv`):

```
mkdir work
cd work/

python -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements_dev.txt
``` 

## How it works

### Getting/setting the auth settings

NOTE: instructions mention `your-domain`. You need to replace it with your actual domain/URL.

To write to a JASMIN Object Store, you need to create a new role with its own access credentials.
Here are instructions to do that:

1. Visit the portal for your domain, e.g.:

    http://your-domain-o.s3.jc.rl.ac.uk:81/_admin/portal/index.html

    (Replace `your-domain` with your atual domain in the above URL).

    Login using your JASMIN Accounts Portal credentials.

2. Add a new token

    - Click the Settings wheel in the top-right, and select "Permissions"
    - Select: "Tokens"
    - Click: "+Add"

    Add a token with details such as:

    - short name: "access-role"
    - Expiry: up to you - select from list
    - S3 Secret Key: tick this option

    Click "Add" to create the token.

3. Copy the credentials

    Copy the output shown on the screen, e.g.:

```
 Success: Token successfully created. Please copy this information for your records.
 Notice: Once you close this message or navigate away from this page, the S3 secret key will not be displayed again!

Token ID: YOUR_TOKEN_FROM_OBJECT_STORE_PORTAL

S3 Secret Key: YOUR_SECRET_FROM_OBJECT_STORE_PORTAL

Expiration Date: 2027-02-01

Owner: your userid

Description: access-role
```

4. Put the details into a credentials file:

    Save the `secret` and `token` in: `~/.credentials/jos-credentials.json`

    E.g.:

```
$ cat ~/.credentials/jos-credentials.json
{
  "secret": "YOUR_SECRET_FROM_OBJECT_STORE_PORTAL",
  "token": "YOUR_TOKEN_FROM_OBJECT_STORE_PORTAL"
}
```

### Using the "minio" python client library
 
This is how it works:

```
# Import required libraries
import os
import json

from minio import Minio
from minio.deleteobjects import DeleteObject

this_dir = "."
STORE_URL = "name-o.s3.jc.rl.ac.uk:80"
BUCKET_ID = "test-bucket-minio"
TEST_FILE_NAME = "test_file.dat"
TEST_FILE_PATH = os.path.join(this_dir, TEST_FILE_NAME)
BUCKET_FILE_PATH = BUCKET_ID + "/" + TEST_FILE_NAME
SIZE = os.path.getsize(TEST_FILE_PATH)

# Load the credentials from your JSON file
CREDS_FILE = os.path.join(os.environ["HOME"], ".credentials/jos-credentials.json")
creds = json.load(open(CREDS_FILE))

# Create client with access and secret key.
m = Minio(STORE_URL, creds["token"], creds["secret"], secure=False)

# Create bucket.
m.make_bucket(BUCKET_ID)

# List buckets
buckets = m.list_buckets()
for bucket in buckets:
    print(bucket.name, bucket.creation_date)

# Put object in the bucket
m.put_object(BUCKET_ID, TEST_FILE_NAME, open(TEST_FILE_PATH, "rb"), length=SIZE)

# List objects
objects = m.list_objects(BUCKET_ID)
for obj in objects:
    print(obj)

# Get an object and write locally
TMP_FILE = "newfile.dat"
resp = m.get_object(BUCKET_ID, TEST_FILE_NAME)
with open(TMP_FILE, "wb") as w:
    w.write(resp.read())

assert open(TMP_FILE).read() == open(TEST_FILE_PATH).read()

# Define a function a recursively delete a bucket (and its contents)
def delete_bucket(BUCKET_ID):
    delete_object_list = map(lambda x: DeleteObject(x.object_name),
        m.list_objects(BUCKET_ID, "", recursive=True))
    errors = m.remove_objects(BUCKET_ID, delete_object_list)
    for error in errors:
        print("error occured when deleting object", error)

    m.remove_bucket(BUCKET_ID)

# Delete the bucket if it exists
if m.bucket_exists(BUCKET_ID):
    delete_bucket(BUCKET_ID)

```


