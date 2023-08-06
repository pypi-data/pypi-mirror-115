from csengine.service import Service
from elasticsearch._async.helpers import async_bulk


class BaseESModelService(Service):
    model = None
    index = None

    def __init__(self, client, index=None, name=None, app=None):
        super().__init__(name=name, app=app)
        self._client = client
        self._index = index or self.index or self.model.__name__.lower()

    def _wrap(self, values):
        return self.model(**values) if values else None


class ESModelService(BaseESModelService):

    def create(self, **values):
        pk = values.get(self.model.Meta.pk_field)
        self._client.index(index=self._index, id=pk, body=values)
        return self._wrap(values)

    def get(self, pk):
        values = self._client.get(self._index, id=pk)['_source']
        return self._wrap(values)

    def save(self, obj):
        pk = getattr(obj, self.model.Meta.pk_field)
        self._client.index(index=self._index, id=pk, body=obj.dict())
        return obj

    def get_dict(self, pk):
        return self._client.get(self._index, id=pk)['_source']

    def select(self, query):
        res = self._client.search(index=self._index, body={"query": query})
        return (self._wrap(hit['_source']) for hit in res['hits']['hits'])


class AsyncESModelService(BaseESModelService):

    async def create(self, **values):
        pk = values.get(self.model.Meta.pk_field)
        await self._client.index(index=self._index, id=pk, body=values)
        return self._wrap(values)

    async def bulk_create(self, values):
        data = (dict({"_index": self._index}, **item) for item in values)
        await async_bulk(self._client, data)
        # return [self.wrap(item) for item in result['items']]

    async def get(self, pk):
        result = await self._client.get(self._index, id=pk)
        return self._wrap(result['_source'])

    async def save(self, obj):
        pk = getattr(obj, self.model.Meta.pk_field)
        await self._client.index(index=self._index, id=pk, body=obj.dict())
        return obj

    async def get_dict(self, pk):
        result = await self._client.get(self._index, id=pk)['_source']
        return result['_source']

    async def select(self, query):
        res = await self._client.search(index=self._index, body={"query": query})
        return [self._wrap(hit['_source']) for hit in res['hits']['hits']]
