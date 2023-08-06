
class Action:

    def __init__(self, view):
        self.view = view
        self.app = view.app

    def execute(self, *args, **kwargs):
        raise NotImplementedError()
