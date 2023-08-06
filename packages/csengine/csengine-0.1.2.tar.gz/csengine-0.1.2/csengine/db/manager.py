import uuid


class ModelManager:

    def __init__(self, model=None, provider=None):
        self._model = model
        self._provider = provider

    def set_model(self, model):
        self._model = model

    def set_provider(self, provider):
        self._provider = provider

    def create(self, **values):
        raise NotImplementedError()

    def get(self, pk):
        return self._provider.get(self._model, pk)

    def select(self, filt):
        raise NotImplementedError()

    def select_object(self, **filt):
        objects = self.select(filt)
        return objects[0] if objects else None

    async def async_create(self, **values):
        raise NotImplementedError()

    async def async_get(self, pk):
        return await self._provider.get(self._model, pk)

    async def async_select(self, filt):
        raise NotImplementedError()

    async def async_select_object(self, **filt):
        objects = await self.async_select(filt)
        return objects[0] if objects else None

    def wrap(self, values):
        return self._model(**values)

    def generate_key(self, **kwargs):
        return uuid.uuid4().hex


class KVModelManager(ModelManager):

    async def async_create(self, **values):
        pk = values.get(self._model.Meta.pk_field) or self.generate_key(**values)
        values = dict(values, **{self._model.Meta.pk_field: pk})
        await self._provider.create(self._model, pk, values)
        return self.wrap(values)

    def create(self, **values):
        pk = values.get(self._model.Meta.pk_field) or self.generate_key(**values)
        values = dict(values, **{self._model.Meta.pk_field: pk})
        self._provider.create(self._model, pk, values)
        return self.wrap(values)
