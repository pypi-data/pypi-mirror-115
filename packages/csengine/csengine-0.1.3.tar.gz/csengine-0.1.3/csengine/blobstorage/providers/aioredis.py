from ..provider import AsyncBlobStorageProvider
from csengine.extentions.redis.clients.aioredis import AioRedisClient


class AioRedisBlobStorageProvider(AsyncBlobStorageProvider):
    client_class = AioRedisClient

    def __init__(self, url, ttl=None):
        super().__init__()
        self._url = url
        self._ttl = ttl
        self._client = self.client_class(url)

    async def init(self):
        return await self._client.init()

    async def _upload(self, name, data, chunk_size=None):
        if not any(isinstance(data, _type) for _type in [bytearray, bytes, float, int, str]):
            data = data.read()
        return await self._client.set(name, data, ttl=self._ttl)

    async def _download(self, name, chunk_size=None):
        return await self._client.get(name)

    async def delete(self, name: str):
        return await self._client.delete(name)
