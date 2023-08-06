
class AppComponent:
    def __init__(self, name=None, app=None):
        self._app = app
        self._name = name or self.__class__.__name__

    async def init(self):
        pass

    async def close(self):
        pass

    @property
    def name(self):
        return self._name

    @property
    def app(self):
        return self._app

    def set_app(self, app):
        self._app = app
