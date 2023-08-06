from fastapi import Request

from .models import SuccessResponse
from .view import FastAPIView, get


class HealthView(FastAPIView):

    @get("/", response_model=SuccessResponse, include_in_schema=False)
    async def health(self, request: Request):
        return SuccessResponse()
