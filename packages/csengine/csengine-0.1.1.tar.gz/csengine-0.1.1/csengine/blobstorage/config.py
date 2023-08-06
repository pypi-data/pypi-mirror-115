from typing import Dict, Any

from pydantic import BaseModel


class StorageConfig(BaseModel):
    provider_class: str
    args: Dict[str, Any]


class Config(BaseModel):
    provider: str
    configs: Dict[str, StorageConfig]
