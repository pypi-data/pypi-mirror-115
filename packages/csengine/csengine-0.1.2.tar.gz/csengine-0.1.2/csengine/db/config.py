from typing import Dict, Any

from pydantic import BaseModel


class Config(BaseModel):
    provider_class: str
    args: Dict[str, Any]
