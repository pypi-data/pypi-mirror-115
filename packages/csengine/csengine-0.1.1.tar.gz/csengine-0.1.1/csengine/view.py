from .component import AppComponent


class View(AppComponent):
    def __init__(self, name=None, app=None):
        super().__init__(name or self.__class__.__name__[:-len('View')], app=app)
