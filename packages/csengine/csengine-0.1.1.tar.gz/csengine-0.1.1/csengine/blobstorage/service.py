from typing import Any

from csengine.service import Service


class BlobStorageService(Service):
    chunk_size_default = 65536

    def __init__(self, provider, name=None, app=None):
        super().__init__(name=name, app=app)
        self._provider = provider

    def upload(self, data: Any, name=None, chunk_size: int = None):
        return self._provider.upload(data, name, chunk_size or self.chunk_size_default)

    def download(self, name: str, dest: str, chunk_size: int = None):
        return self._provider.download(name, dest, chunk_size or self.chunk_size_default)

    def delete(self, name: str):
        return self._provider.delete(name)


class AsyncBlobStorageService(Service):
    chunk_size_default = 65536

    def __init__(self, provider, name=None, app=None):
        super().__init__(name=name, app=app)
        self._provider = provider

    async def upload(self, data: Any, name=None, chunk_size: int = None):
        return await self._provider.upload(data, name, chunk_size or self.chunk_size_default)

    async def download(self, name: str, dest: str, chunk_size: int = None):
        return await self._provider.download(name, dest, chunk_size or self.chunk_size_default)

    async def delete(self, name: str):
        return await self._provider.delete(name)
