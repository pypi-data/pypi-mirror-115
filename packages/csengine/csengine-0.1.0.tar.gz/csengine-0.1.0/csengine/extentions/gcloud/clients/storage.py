import io
import os
from typing import Any

from google.cloud import storage

from ..client import BaseGCloudStorageClient


class GCloudStorageClient(BaseGCloudStorageClient):

    def __init__(self):
        self._client = storage.Client()

    def upload(self, bucket: str, name: str, values: Any, chunk_size=None):
        bucket = self._client.bucket(bucket)
        blob = bucket.blob(name)
        if not hasattr(values, 'read'):
            values = io.StringIO(values)
        blob.upload_from_file(values)
        return name

    def download(self, bucket: str, name: str, dest: str, chunk_size: int = None):
        os.makedirs(dest, exist_ok=True)
        bucket = self._client.bucket(bucket)
        file_name = os.path.join(dest, name)
        blob = bucket.blob(name)
        blob.download_to_filename(file_name)
        return file_name

    def delete(self, bucket: str, name: str):
        bucket = self._client.bucket(bucket)
        blob = bucket.blob(name)
        blob.delete()
