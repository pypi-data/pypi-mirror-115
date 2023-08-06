import json


class Observable(object):
    def __init__(self):
        self._observers = {}

    def subscribe(self, event, observer):
        if event not in self._observers:
            self._observers[event] = []
        self._observers[event].append(observer)

    def notify(self, notification):
        for observer in self._observers.get(notification.name, []):
            observer.handle_notification(notification)


class AsyncObservable(Observable):
    async def notify(self, notification):
        for observer in self._observers.get(notification.name, []):
            await observer.handle_notification(notification)


class Observer(object):
    def handle_notification(self, notification):
        raise NotImplementedError()


class Notification(object):
    def __init__(self, name, body=None, _type=None):
        """
        Constructor.

        @param name: name of the Notification instance. (required)
        @param body: the Notification body. (optional)
        @param _type: the type of the Notification (optional)
        """
        self._name = name
        self._body = body
        self._type = _type

    def __str__(self):
        return 'Notification(name={}, body={}, type={})'.format(self._name, self._body, self._type)

    def __repr__(self):
        bd = "None" if self._body is None else repr(self._body)
        ty = "None" if self._type is None else repr(self._type)

        msg = "Notification Name: " + self.name
        msg += "\nBody:"+bd
        msg += "\nType:"+ty

        return msg

    @property
    def name(self):
        return self._name

    @property
    def body(self):
        return self._body

    @property
    def type(self):
        return self._type

    @property
    def json(self):
        return json.dumps({
           'name': self._name,
           'body': self._body,
           'type': self._type,
        })


class Event(Notification):
    def __init__(self, name, body=None):
        super().__init__(name, body=body, _type='event')
