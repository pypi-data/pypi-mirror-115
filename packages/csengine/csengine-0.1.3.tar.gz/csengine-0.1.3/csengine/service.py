from .component import AppComponent


class Service(AppComponent):
    def __init__(self, name=None, app=None):
        super().__init__(name or self.__class__.__name__[:-len('Service')], app=app)
