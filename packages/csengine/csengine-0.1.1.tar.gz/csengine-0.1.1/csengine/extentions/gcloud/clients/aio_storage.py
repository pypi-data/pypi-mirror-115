import io
import os
from typing import Any

import aiohttp
from gcloud.aio.storage import Storage

from ..client import BaseGCloudStorageClient


class AioGCloudStorageClient(BaseGCloudStorageClient):

    def __init__(self, session=None, conn_timeout=None, read_timeout=None,  options=None):
        super().__init__()
        self._session = session
        self._storage = None
        self._conn_timeout = conn_timeout
        self._read_timeout = read_timeout
        self._options = options or {}

    async def init(self):
        options = self._options.copy()
        if self._conn_timeout:
            options['conn_timeout'] = self._conn_timeout
        if self._read_timeout:
            options['read_timeout'] = self._read_timeout
        self._session = aiohttp.ClientSession()
        self._storage = Storage(session=self._session, **options)

    async def upload(self, bucket: str, name: str, values: Any, chunk_size: int = None):
        if not any(isinstance(values, _type) for _type in [bytes, str, io.IOBase]):
            values = values.read()
        return await self._storage.upload(bucket, name, values)

    async def download(self, bucket: str, name: str, dest: str, chunk_size: int = None):
        os.makedirs(dest, exist_ok=True)
        image = await self._storage.download(bucket, name)
        file_name = os.path.join(dest, name)
        with open(file_name, 'wb') as f:
            f.write(image)
        return file_name

    async def delete(self, bucket: str, name: str):
        return await self._storage.delete(bucket, name)

    async def close(self):
        # Session could be None if FileStorage wasn't used during app run
        await self._storage.session.close()
