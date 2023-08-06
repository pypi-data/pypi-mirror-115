from typing import Any

from pydantic.main import BaseModel


class BaseSerializer(BaseModel):

    class Meta:
        pass

    def __init__(self, **data: Any):
        view = data.pop('view')
        super().__init__(**data)
        object.__setattr__(self, 'view', view)
        object.__setattr__(self, 'app', view.app)

    async def validate_data(self):
        raise NotImplementedError()
