from typing import Any, Dict, List

from pydantic import BaseModel, Field


class SuccessResponse(BaseModel):
    code: int = Field(200, title="HTTP Status code")


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Dict[str, Any] = None
    meta: Dict[str, Any] = None
    args: List[Any] = None
