import prometheus_client
from fastapi import Response, Request
from .view import FastAPIView, get


class MetricsView(FastAPIView):

    @get("/metrics", include_in_schema=False)
    async def metrics(self, request: Request):
        return Response(content=prometheus_client.generate_latest(),
                        media_type=prometheus_client.CONTENT_TYPE_LATEST)
