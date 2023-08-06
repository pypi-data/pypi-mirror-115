from .component import AppComponent
from .observer import Observer


class Command(AppComponent, Observer):
    def __init__(self, name=None, app=None):
        super().__init__(name or self.__class__.__name__[:-len('Command')], app=app)

    def execute(self, notification):
        raise NotImplementedError()

    def handle_notification(self, notification):
        return self.execute(notification)


class AsyncCommand(Command):
    def __init__(self, name=None, app=None):
        super().__init__(name or self.__class__.__name__[:-len('Command')], app=app)

    async def execute(self, notification):
        raise NotImplementedError()

    async def handle_notification(self, notification):
        return await self.execute(notification)


