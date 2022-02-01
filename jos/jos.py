"""
jos.py
======

JASMIN object store client class: JASMINObjectStore.
"""


__author__ = """Ag Stephens"""
__contact__ = 'ag.stephens@stfc.ac.uk'
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"


import os
import json

import boto3
import botocore
import s3fs


class JASMINObjectStore:

    def __init__(self, store_url=None, creds=None, creds_file=None):
        """[summary]

        Args:
            store_url ([type], optional): [description]. Defaults to None.
            creds ([type], optional): [description]. Defaults to None.
            creds_file ([type], optional): [description]. Defaults to None.
        """

        if creds_file:
            self._creds = self._parse_creds_file(creds_file)
        else:
            self._creds = creds

        # If store url not provided, must get from creds, or fail
        if not store_url:
            if "store_url" not in self._creds:
                raise Exception("Must provide 'store_url' as argument or in credentials.")
            self._store_url = self._creds["store_url"]
        else:
            self._store_url = store_url

        self._setup_fs()

    def _setup_fs(self):
        if self._creds:
            self._fs = s3fs.S3FileSystem(
                anon=False,
                secret=self._creds["secret"],
                key=self._creds["token"],
                client_kwargs={"endpoint_url": self._store_url},
                config_kwargs={"max_pool_connections": 50},
            )
        else:
            self._fs = s3fs.S3FileSystem(
                anon=True,
                client_kwargs={"endpoint_url": self._store_url},
                config_kwargs={"max_pool_connections": 50},
            )

    def _parse_creds_file(self, creds_file):
        return json.load(open(creds_file))

    def create_bucket(self, bucket_id, policy="open"):
        """
        
        Args:
            bucket_id ([type]): [description]
            policy (str, optional): [description]. Defaults to "open".
        """
        if not self._fs.exists(bucket_id):
            self._fs.mkdir(bucket_id)

    def _list(self, item, detail=False):
        """[summary]

        Args:
            detail (bool, optional): [description]. Defaults to False.
        """
        if detail:
            return self._fs.listdir(item)
        else:
            return self._fs.ls(item)

    def list_buckets(self, detail=False):
        """
        
        """
        return self._list("", detail)

    def list_bucket(self, bucket_id, detail=False):
        """[summary]

        Args:
            bucket_id ([type]): [description]
        """
        return self._list(bucket_id, detail)

    def delete_bucket(self, bucket_id):
        """
        

        Args:
            bucket_id ([type]): [description]
        """
        try:
            self._fs.delete(bucket_id, recursive=True)
        except Exception:
            raise Exception(f"Cannot delete bucket: {bucket_id}")

    def put_file(self, bucket_id, file_id):
        """
        

        Args:
            bucket_id ([type]): [description]
            file_id ([type]): [description]
        """
        self._fs.put(file_id, bucket_id + "/" + file_id)

    def get_file(self, bucket_id, file_id, target_dir):
        """[summary]

        Args:
            bucket_id ([type]): [description]
            file_id ([type]): [description]
        """
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

        self._fs.get(bucket_id + "/" + file_id, target_dir + "/" + file_id)

    # async get_files(self, bucket_id, file_ids, parallel_count=10):
    #     """[summary]

    #     Args:
    #         self ([type]): [description]
    #         bucket_id ([type]): [description]
    #         file_ids ([type]): [description]
    #         parallel_count (int, optional): [description]. Defaults to 10.
    #     """
    #     return files


