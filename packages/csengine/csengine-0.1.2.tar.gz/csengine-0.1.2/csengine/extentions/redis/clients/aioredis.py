import aioredis

from csengine.extentions.redis.client import BaseRedisClient


class AioRedisClient(BaseRedisClient):

    async def init(self):
        self._connection = await aioredis.create_pool(self._url, minsize=1, maxsize=5)

    async def set_dict(self, name, value, ttl=None):
        value_list = []
        for k, v in value.items():
            value_list.extend([k, v])
        await self._connection.execute('hmset', name, *value_list)
        await self.set_expiration(name, ttl)
        return value

    async def get_dict(self, name):
        value_list = await self._connection.execute('hgetall', name)
        return dict(zip(value_list[::2], value_list[1::2]))

    async def set(self, name, value, ttl=None):
        await self._connection.execute('set', name, value)
        await self.set_expiration(name, ttl)
        return value

    async def get(self, name):
        return await self._connection.execute('get', name)

    async def delete(self, *names):
        return await self._connection.execute('del', *names)

    async def hset(self, name, value, ttl=None):
        await self._connection.execute('hset', name, value)
        await self.set_expiration(name, ttl)
        return value

    async def hget(self, name):
        return await self._connection.execute('hget', name)

    async def hmset(self, name, values, ttl=None):
        await self._connection.execute('hmset', name, values)
        await self.set_expiration(name, ttl)
        return values

    async def hmget(self, name):
        return await self._connection.execute('hmget', name)

    async def hgetall(self, name):
        return await self._connection.execute('hgetall', name)

    async def mget(self, *keys):
        return await self._connection.execute('mget', *keys)

    async def execute(self, *args, **kwargs):
        return await self._connection.execute(*args, **kwargs)

    async def set_expiration(self, name, ttl=None):
        ttl = ttl or self._ttl
        if ttl:
            await self._connection.execute('expire', name, ttl)
