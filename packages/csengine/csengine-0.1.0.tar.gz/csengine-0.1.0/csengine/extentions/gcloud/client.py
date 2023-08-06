from typing import Any


class BaseGCloudStorageClient:

    def init(self):
        pass

    def upload(self, bucket: str, name: str, values: Any, chunk_size: int = None):
        raise NotImplementedError()

    def download(self, bucket: str, name: str, dest: str, chunk_size: int = None):
        raise NotImplementedError()

    def delete(self, bucket: str, name: str):
        raise NotImplementedError()

    def close(self):
        pass
