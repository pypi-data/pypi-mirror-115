from csengine.observer import Event


class ActionStartedEvent(Event):

    def __init__(self, action, request, args, kwargs):
        super().__init__('ACTION_STARTED', {'action': action, 'request': request,
                                           'args': args, 'kwargs': kwargs})

    @property
    def action_name(self):
        return self.action.__name__

    @property
    def action(self):
        return self.body['action']

    @property
    def request(self):
        return self.body['request']

    @property
    def args(self):
        return self.body['args']

    @property
    def kwargs(self):
        return self.body['kwargs']
