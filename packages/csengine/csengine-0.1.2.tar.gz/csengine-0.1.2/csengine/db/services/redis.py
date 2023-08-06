import json
import uuid

from csengine.service import Service


class RedisModelService(Service):
    model = None

    def __init__(self, client, name=None, app=None):
        super().__init__(name=name, app=app)
        self._client = client

    def create(self, **values):
        pk = values.get(self.model.Meta.pk_field) or self.generate_key(**values)
        values = dict(values, **{self.model.Meta.pk_field: pk})
        self._client.set(self.get_redis_key(pk), json.dumps(values))
        return self.model(**values)

    def get(self, pk):
        values = self._client.get(self.get_redis_key(pk))
        return self.model(**json.loads(values)) if values else None

    def delete(self, *pks):
        pks = [self.get_redis_key(pk) for pk in pks]
        return self._client.delete(*pks)

    def save(self, obj):
        pk = getattr(obj, self.model.Meta.pk_field)
        self._client.set(self.get_redis_key(pk), json.dumps(obj.dict()))
        return obj

    def get_vo(self, pk):
        values = self._client.get(self.get_redis_key(pk))
        return json.loads(values) if values else None

    def get_redis_key(self, id):
        return f'{self.model.__name__}:{id}'

    def generate_key(self, **kwargs):
        return uuid.uuid4().hex
