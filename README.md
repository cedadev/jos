# jos - a JASMIN Object Store Client library

A client library and command-line tool for interacting with the JASMIN Object Store.

* Free software: BSD - see LICENCE file in top-level package directory

## Installation

Simple installation using a virtual environment (`venv`):

```
mkdir work
cd work/

git clone https://github.com/cedadev/jos
cd jos

python -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt

python setup.py develop
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

### Command-line

From the command-line:

```
# Ensure you have the credentials file set up

$ cat ~/.credentials/jos-credentials.json
{
  "secret": "YOUR_SECRET_FROM_OBJECT_STORE_PORTAL",
  "token": "YOUR_TOKEN_FROM_OBJECT_STORE_PORTAL"
}

# Define some variables to demonstrate the workflow
TEST_FILE_NAME="my-file.dat"
BUCKET_ID="my-test-bucket"
BUCKET_FILE_PATH=${BUCKET_ID}/${TEST_FILE_NAME}
TARGET_DIR=mytmpdir
STORE_URL=http://your-domain-o.s3.jc.rl.ac.uk/

# See command help
jos --help

# Create bucket
jos create-bucket -s $STORE_URL $BUCKET_ID

# List all buckets
jos list-buckets -s $STORE_URL

# List specific bucket contents
jos list-bucket -s $STORE_URL $BUCKET_ID

# Put a file into the object store
jos put -s $STORE_URL -b $BUCKET_ID $TEST_FILE_PATH

# Get a file from the object store
jos get -s $STORE_URL -b $BUCKET_ID -t $TARGET_DIR $TEST_FILE_NAME

# Delete a bucket
jos delete-bucket -s $STORE_URL $BUCKET_ID

```

### Using the python client library
 
This is how it works:

```
import os
import time

from jos import JASMINObjectStore

CREDS_FILE = "my-credentials.json" # or use default: "~/.credentials/jos-credentials.json"
STORE_URL = "http://your-domain-o.s3.jc.rl.ac.uk/"
BUCKET_ID = "my-test-bucket"
TEST_FILE_NAME = "test_file.dat"
TEST_FILE_PATH = os.path.join("my-dir", TEST_FILE_NAME)
TARGET_DIR = "mytmpdir"
BUCKET_FILE_PATH = BUCKET_ID + "/" + TEST_FILE_NAME
SIZE = os.path.getsize(TEST_FILE_PATH)

# Create an instance of the object store to interact with
j = JASMINObjectStore(STORE_URL, creds_file=CREDS_FILE)

# Create a bucket
j.create_bucket(BUCKET_ID)

# Put a file in the object store
j.put_file(BUCKET_ID, TEST_FILE_PATH)

# List content of all buckets
buckets = j.list_buckets()

# List content of all buckets with details
records = j.list_buckets(details=True)

# List content of specific bucket
content = j.list_bucket(BUCKET_ID)

# List content of specific bucket with details
records = j.list_bucket(BUCKET_ID, details=True)

# Get an object from object store
tmpfile = os.path.join(target_dir, TEST_FILE_NAME)
j.get_file(BUCKET_ID, TEST_FILE_NAME, target_dir.as_posix())

# Delete bucket
if j._fs.exists(BUCKET_ID):
    j.delete_bucket(BUCKET_ID)

```

## Anonymous usage - without access credentials

TBA

## Credits

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.


