import json

from ..provider import BaseRedisProvider
from csengine.extentions.redis.clients.redis import RedisClient


class RedisProvider(BaseRedisProvider):
    client_class = RedisClient

    def create(self, model, key, values):
        return self._client.set(key, json.dumps(values))

    def get(self, model, key):
        values = self._client.get(self.get_redis_key(model, key))
        return json.loads(values) if values else None
