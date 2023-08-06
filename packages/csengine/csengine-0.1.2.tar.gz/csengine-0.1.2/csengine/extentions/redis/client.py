
class BaseRedisClient:

    def __init__(self, url, ttl=None):
        self._url = url
        self._connection = None
        self._ttl = ttl

    def init(self):
        pass

    def set(self, name, value):
        raise NotImplementedError()

    def get(self, name):
        raise NotImplementedError()

    def delete(self, *names):
        raise NotImplementedError()

    def set_dict(self, name, value, ttl=None):
        raise NotImplementedError()

    def get_dict(self, name):
        raise NotImplementedError()

    def hset(self, name, value):
        raise NotImplementedError()

    def hget(self, name):
        raise NotImplementedError()

    def hmset(self, name, values, ttl=None):
        raise NotImplementedError()

    def hmget(self, name):
        raise NotImplementedError()

    def hgetall(self, name):
        raise NotImplementedError()

    def execute(self, *args, **kwargs):
        raise NotImplementedError()

    def set_expiration(self, name, ttl=None):
        raise NotImplementedError()
