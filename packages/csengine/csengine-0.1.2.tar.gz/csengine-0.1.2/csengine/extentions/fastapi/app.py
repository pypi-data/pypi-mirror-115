import logging

from fastapi import FastAPI
from csengine.app import App
from csengine.observer import AsyncObservable
from starlette.middleware.cors import CORSMiddleware
from starlette_prometheus import PrometheusMiddleware
from csengine.extentions.fastapi.view.health import HealthView
from csengine.extentions.fastapi.view.metrics import MetricsView
from csengine.extentions.fastapi.view.system import SystemInfoView

log = logging.getLogger(__name__)


class FastAPIApp(App):
    event_manager_class = AsyncObservable

    def __init__(self, fast_api: FastAPI):
        super().__init__()
        self._fast_api = fast_api
        self._health_view = None
        self._metrics_view = None
        self._system_info_view = None
        self.common_dependencies = []

        # add App event handlers
        fast_api.on_event('startup')(self.on_init)
        fast_api.on_event('shutdown')(self.on_close)

    def include_router(self, view, dependencies = None, **kwargs):
        dependencies = dependencies or []
        dependencies += self.common_dependencies
        return self._fast_api.include_router(view.get_router(), dependencies=dependencies, **kwargs)

    def add_cors(self, allow_origins=None, allow_credentials=True, allow_methods=None,
                 allow_headers=None):
        allow_origins = allow_origins or ['*']
        allow_methods = allow_methods or ['*']
        allow_headers = allow_headers or ['*']
        self._fast_api.add_middleware(CORSMiddleware, allow_origins=allow_origins,
                                      allow_credentials=allow_credentials,
                                      allow_methods=allow_methods, allow_headers=allow_headers)

    def add_health_check(self, view_class=None, tags=None):
        view_class = view_class or HealthView
        tags = tags or ['Common']
        self._health_view = self.register_view(view_class())
        self._fast_api.include_router(self._health_view.get_router(), tags=tags, prefix='/health')
        self._fast_api.include_router(self._health_view.get_router(), tags=tags)

    def add_metrics(self, view_class=None, tags=None, dependencies=None):
        view_class = view_class or MetricsView
        tags = tags or ['Common']
        self._fast_api.add_middleware(PrometheusMiddleware)
        self._metrics_view = self.register_view(view_class())
        self._fast_api.include_router(self._metrics_view.get_router(), tags=tags,
                                      dependencies=dependencies)

    def add_system_info(self, view_class=None, tags=None, dependencies=None):
        view_class = view_class or SystemInfoView
        tags = tags or ['Common']
        self._system_info_view = self.register_view(view_class())
        self._fast_api.include_router(self._system_info_view.get_router(), tags=tags,
                                      dependencies=dependencies)

    async def notify(self, notification):
        return await self._event_manager.notify(notification)

    async def on_init(self):
        log.info('App initializing.')
        for client in self._clients.values():
            await client.init()
        for service in self._services.values():
            await service.init()
        for view in self._views.values():
            await view.init()

    async def on_close(self):
        log.info('App closing.')
        for service in self._services.values():
            await service.close()
        for view in self._views.values():
            await view.close()

    @property
    def fast_api(self):
        return self._fast_api
