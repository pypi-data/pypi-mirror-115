from ..provider import BlobStorageProvider
from csengine.extentions.gcloud.clients.storage import GCloudStorageClient


class CloudBlobStorageProvider(BlobStorageProvider):
    client_class = GCloudStorageClient

    def __init__(self, bucket, conn_timeout=None, read_timeout=None):
        super().__init__()
        self._bucket = bucket
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._client = self.client_class()

    def _upload(self, name, data, chunk_size=None):
        return self._client.upload(self._bucket, name, data, chunk_size=chunk_size)

    def download(self, name: str, dest: str, chunk_size: int = None):
        return self._client.download(self._bucket, name, dest, chunk_size)

    def delete(self, name: str):
        return self._client.delete(name)