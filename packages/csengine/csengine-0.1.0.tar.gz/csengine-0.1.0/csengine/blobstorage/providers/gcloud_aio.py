from ..provider import AsyncBlobStorageProvider
from csengine.extentions.gcloud.clients.aio_storage import AioGCloudStorageClient


class AioCloudBlobStorageProvider(AsyncBlobStorageProvider):
    client_class = AioGCloudStorageClient

    def __init__(self, bucket, conn_timeout=None, read_timeout=None):
        super().__init__()
        self._bucket = bucket
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout

    async def init(self):
        self._client = self.client_class(conn_timeout=self._conn_timeout,
                                         read_timeout=self._read_timeout)
        return await self._client.init()

    async def _upload(self, name, data, chunk_size=None):
        return await self._client.upload(self._bucket, name, data, chunk_size)

    async def download(self,  name, dest, chunk_size=None):
        return await self._client.download(self._bucket, name, dest, chunk_size=chunk_size)

    async def delete(self, name: str):
        return await self._client.delete(self._bucket, name)
