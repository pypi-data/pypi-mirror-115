from elasticsearch import AsyncElasticsearch
from elasticsearch._async.helpers import async_bulk


class AsyncESProvider(BaseESProvider):
    client_class = AsyncElasticsearch

    async def create(self, model, key, values):
        pk = values.get(self._get_pk_field(model))
        await self._client.index(index=self._get_index(model), id=pk, body=values)
        return self._wrap(model, values)

    async def bulk_create(self, model, values):
        index = self._get_index(model)
        data = (dict({"_index": index}, **item) for item in values)
        await async_bulk(self._client, data)
        # return [self.wrap(item) for item in result['items']]

    async def save(self, model, obj):
        pk = getattr(obj, self._get_pk_field(model))
        await self._client.index(index=self._get_index(model), id=pk, body=obj.dict())
        return obj

    async def get(self, model, pk):
        result = await self._client.get(self._get_index(model), id=pk)
        return self.wrap(model, result['_source'])

    async def get_dict(self, model, pk):
        result = await self._client.get(self._get_index(model), id=pk)
        return result['_source'] if result else None

    async def select(self, model, query):
        res = await self._client.search(index=self._get_index(model), body={"query": query})
        return [self.wrap(model, hit['_source']) for hit in res['hits']['hits']]

    async def select_dict_objects(self, model, query):
        res = await self._client.search(index=self._get_index(model), body={"query": query})
        return [hit['_source'] for hit in res['hits']['hits']]
