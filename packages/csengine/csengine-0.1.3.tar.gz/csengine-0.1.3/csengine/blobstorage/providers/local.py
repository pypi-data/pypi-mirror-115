import os
import shutil
from typing import Any

from ..provider import BlobStorageProvider


class LocalFSBlobProvider(BlobStorageProvider):
    def __init__(self, root_dir):
        super().__init__()
        self._root_dir = root_dir
        # shutil.rmtree(self._root_dir, ignore_errors=True)
        os.makedirs(self._root_dir, exist_ok=True)

    def upload(self, data: Any, name=None, chunk_size: int = None):
        file_name = os.path.join(self._root_dir, name)
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        if isinstance(data, bytes):
            open(file_name, "wb").write(data)
        else:
            with open(file_name, "wb") as f:
                for chunk in iter(lambda: data.read(chunk_size), b''):
                    f.write(chunk)

    def download(self, name, dest, chunk_size=65536):
        file_name = os.path.join(self._root_dir, name)
        shutil.copy2(file_name, dest)
        return file_name

    def delete(self, name: str):
        file_name = os.path.join(self._root_dir, name)
        if os.path.exists(file_name):
            os.remove(file_name)
