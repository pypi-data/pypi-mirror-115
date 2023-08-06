from fastapi import Request

from csengine.utils.package import get_packages
from .view import FastAPIView, get


class SystemInfoView(FastAPIView):
    roles = ['Admin']

    @get('/system-info')
    async def get_info(self, request: Request):
        return {'packages': get_packages()}
