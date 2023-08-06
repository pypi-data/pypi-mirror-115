from ..provider import BlobStorageProvider
from csengine.extentions.redis.clients.redis import RedisClient


class RedisBlobStorageProvider(BlobStorageProvider):
    client_class = RedisClient

    def __init__(self, url, ttl=None):
        super().__init__()
        self._ttl = ttl
        self._client = self.client_class(url)

    def _upload(self, name, data, chunk_size=None):
        if not any(isinstance(data, _type) for _type in [bytearray, bytes, float, int, str]):
            data = data.read()
        return self._client.set(name, data)

    def _download(self, name, chunk_size=None):
        return self._client.get(name)

    def delete(self, name: str):
        return self._client.delete(name)

