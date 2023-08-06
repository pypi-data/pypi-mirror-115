from pydantic import BaseModel

from csengine.db.config import Config
from csengine.utils.import_util import import_path


class DBProvider:
    client_class = None

    def __init__(self, client=None, **kwargs):
        self._client = client
        self._models = {}

    def register_model(self, model):
        if model.__name__ in self._models:
            return
        if hasattr(model, 'Meta') and hasattr(model.Meta, 'manager_class'):
            self._models[model.__name__] = model
            manager_class = import_path(model.Meta.manager_class)
            model.manager = manager_class(model=model, provider=self)

    def register_models(self, module):
        for item_name, item in module.__dict__.items():
            if isinstance(item, type) and issubclass(item, BaseModel) and item != BaseModel:
                self.register_model(item)

    def set_client(self, client):
        self._client = client

    def create(self, model, key, values):
        raise NotImplementedError()

    def get(self, model, key):
        raise NotImplementedError()


class BaseRedisProvider(DBProvider):

    def __init__(self, url, ttl=None):
        super().__init__()
        self._url = url
        self._ttl = ttl
        self._client = self.client_class(url)

    @staticmethod
    def get_redis_key(model, id):
        return f'{model.__name__}:{id}'


class BaseESProvider(DBProvider):

    @classmethod
    def _wrap(cls, model, values):
        return model(**values) if values else None

    @classmethod
    def _get_index(cls, model):
        return model.Meta.index if hasattr(model.Meta, "index") else model.__name__.lower()

    @classmethod
    def _get_pk_field(cls, model):
        return model.Meta.pk_field


class DBProviderFactory:

    @classmethod
    def build(cls, config):
        config = Config(**config)
        provider_class = import_path(config.provider_class)
        return provider_class(**config.args)
