# Minio:  Python library and command-line tool (mc) 

## 1. Python library: minio

### Installation
  
Simple installation using a virtual environment (`venv`):

```
mkdir work
cd work/

python -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements_dev.txt
``` 

### Getting/setting the authorisation tokens

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
STORE_URL = "mystore-o.s3.jc.rl.ac.uk:80"
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
m.fput_object(BUCKET_ID, TEST_FILE_NAME, TEST_FILE_PATH)

# List objects
objects = m.list_objects(BUCKET_ID)
for obj in objects:
    print(obj.object_name)

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

## 2. Simple introduction to Minio command-line tool: mc

### Installation

On linux, just download binary and change permissions:

```
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod u+x mc
```

And maybe add to `$PATH` environment variable:

```
export PATH=$PATH:${PWD}
```

### Add an object store with an alias

If you plan to interact with an object store, the simplest approach is to tell
`mc` an alias that you want to use that includes information about the:
- object store URL
- access token
- access secret

```
mc alias set mystore <url> <token> <secret> --api S3v4
```

On the JASMIN Object Store, the `<url>` will be something like: 
`http://myproject-o.s3.jc.rl.ac.uk`

### Start interacting with the object store

List all buckets:

```
mc ls mystore
```

Make a bucket:

```
mc mb mystore/mybucket
```

Upload (i.e. "PUT") a file into the new bucket:

```
mc cp output-1.txt mystore/mybucket
```

List all buckets (to see the change):

```
mc ls mystore
```

List the objects in your bucket:

```
mc ls mystore/mybucket
```

Delete everything inside a bucket:

```
mc rm --recursive --force mystore/mybucket
```

Find all files within a bucket matching a pattern, and list them:

```
mc find mystore/mybucket --regex ".*.txt" --exec "mc ls {}"
```

Find all files within a bucket matching a pattern, and copy (i.e. "GET") them
to a local directory:

```
mc find mystore/mybucket --regex ".*.txt" --exec "mc cp {} target/dir/"
```

Stream the contents of an object into a Unix Pipe for processing:

```
mc cat mystore/mybucket/random/a.txt | sed 's/a/b/g'
```



