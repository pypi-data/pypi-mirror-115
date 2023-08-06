from csengine.service import Service


class AsyncModelService(Service):
    model = None

    async def create(self, **values):
        return await self.model.manager.async_create(**values)

    async def select(self, filt):
        return await self.model.manager.async_select(filt)

    async def select_object(self, filt):
        return await self.model.manager.async_select_object(filt)

    async def get(self, pk):
        return await self.model.manager.async_get(pk)

    async def save(self, obj):
        return await self.model.manager.async_save(obj)


class ModelService(Service):
    model = None

    def create(self, **values):
        return self.model.manager.create(**values)

    def select(self, filt):
        return self.model.manager.select(filt)

    def select_object(self, filt):
        return self.model.manager.select_object(filt)

    def get(self, pk):
        return self.model.manager.get(pk)

    def save(self, obj):
        return self.model.manager.save(obj)


class DataModelService(Service):
    model = None
    data = None
    pk_field = None

    def select(self, **filt):
        instances = (self.model(**item) for item in self.data)
        for key, value in filt.items():
            instances = filter(lambda dt: getattr(dt, key, None) == value, instances)
        return list(instances)

    def select_object(self, **filt):
        instances = self.select(**filt)
        return instances[0] if instances else None

    def get(self, pk=None):
        pk_field = self.pk_field or self.model.Meta.pk_field
        instances = self.select(**{pk_field: pk})
        return instances[0] if instances else None

    def select_vos(self, **filt):
        return [obj.dict() for obj in self.select(**filt)]

    def select_vo(self, **filt):
        instance = self.select_object(**filt)
        return instance.dict() if instance else None

    def get_vo(self, pk=None):
        instance = self.get(pk)
        return instance.dict() if instance else None
