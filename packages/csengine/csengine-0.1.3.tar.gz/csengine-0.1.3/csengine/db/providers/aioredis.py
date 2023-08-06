import json

from ..provider import BaseRedisProvider
from csengine.extentions.redis.clients.aioredis import AioRedisClient


class AioRedisProvider(BaseRedisProvider):
    client_class = AioRedisClient

    async def init(self):
        return await self._client.init()

    async def create(self, model, key, values):
        return await self._client.set(self.get_redis_key(model, key), json.dumps(values))

    async def get(self, model, key):
        values = await self._client.get(self.get_redis_key(model, key))
        return json.loads(values) if values else None
