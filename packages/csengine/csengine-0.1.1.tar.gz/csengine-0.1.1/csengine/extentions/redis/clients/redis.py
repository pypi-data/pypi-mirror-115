import redis

from csengine.extentions.redis.client import BaseRedisClient


class RedisClient(BaseRedisClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._connection = redis.from_url(self._url)

    def set_dict(self, name, value, ttl=None):
        self._connection.hmset(name, value)
        self.set_expiration(name, ttl)
        return value

    def get_dict(self, name):
        value_list = self._connection.hgetall(name)
        return dict(zip(value_list[::2], value_list[1::2]))

    def set(self, name, value, ttl=None):
        self._connection.set(name, value)
        if ttl:
            self._connection.expire(name)
        return value

    def get(self, name):
        return self._connection.get(name)

    def delete(self, *names):
        return self._connection.delete(*names)

    def hset(self, name, value, ttl=None):
        self._connection.hset(name, value)
        return value

    def hget(self, name):
        return self._connection.hget(name)

    def hmset(self, name, values, ttl=None):
        self._connection.hmset(name, values)
        self.set_expiration(name, ttl)
        return values

    def hmget(self, name):
        return self._connection.hmget(name)

    def mget(self, *keys):
        return self._connection.mget(*keys)

    def hgetall(self, name):
        return self._connection.hgetall(name)

    def execute(self, *args, **kwargs):
        return self._connection.execute_command(*args, **kwargs)

    def set_expiration(self, name, ttl=None):
        ttl = ttl or self._ttl
        if ttl:
            self._connection.expire(name)
