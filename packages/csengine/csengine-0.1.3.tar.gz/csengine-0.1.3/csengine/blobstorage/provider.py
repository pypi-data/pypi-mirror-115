import os
import uuid
from typing import Any

from csengine.utils.import_util import import_path

from csengine.blobstorage.config import Config


class BaseBlobStorageProvider:
    client_class = None

    def __init__(self, client=None):
        self._client = client

    def upload(self, data: Any, name=None, chunk_size: int = None):
        raise NotImplementedError()

    def download(self, name: str, dest: str, chunk_size: int = None):
        raise NotImplementedError()

    def delete(self, name: str):
        raise NotImplementedError()

    @staticmethod
    def generate_name(data):
        return uuid.uuid4().hex


class BlobStorageProvider(BaseBlobStorageProvider):

    def upload(self, data: Any, name=None, chunk_size: int = None):
        name = name or self.generate_name(data)
        self._upload(name, data)
        return name

    def download(self, name: str, dest: str, chunk_size: int = None):
        os.makedirs(dest, exist_ok=True)
        data = self._download(name)
        file_name = os.path.join(dest, name)
        with open(file_name, 'wb') as f:
            f.write(data)
        return file_name

    def _upload(self, name, data, chunk_size=None):
        raise NotImplementedError()

    def _download(self, name):
        raise NotImplementedError()


class AsyncBlobStorageProvider(BaseBlobStorageProvider):

    async def upload(self, data: Any, name=None, chunk_size: int = None):
        name = name or self.generate_name(data)
        await self._upload(name, data, chunk_size=chunk_size)
        return name

    async def download(self, name: str, dest: str, chunk_size: int = None):
        os.makedirs(dest, exist_ok=True)
        image = await self._download(name, chunk_size=chunk_size)
        file_name = os.path.join(dest, name)
        with open(file_name, 'wb') as f:
            f.write(image)
        return file_name

    async def _upload(self, name, data, chunk_size=None):
        raise NotImplementedError()

    async def _download(self, name, chunk_size=None):
        raise NotImplementedError()


class BlobStorageProviderFactory:

    @classmethod
    def build(cls, config):
        config = Config(**config)
        provider_config = config.configs[config.provider]
        provider_class = import_path(provider_config.provider_class)
        return provider_class(**provider_config.args)
