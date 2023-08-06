import logging

from .command import Command
from .observer import Observable
from .service import Service
from .view import View

log = logging.getLogger(__name__)


class App:
    """Facade class initializes and caches native Application, Services (Model component) and
    View Components, and provides a single place to access to them.

    Services expose an API for manipulating the Data Model
    (including data retrieved from remote services).

    View components deal with API Endpoinds.
    """
    event_manager_class = Observable

    def __init__(self):
        self._clients = {}
        self._services = {}
        self._views = {}
        self._commands = {}
        self._event_manager = self._create_event_manager()

    def _create_event_manager(self):
        return self.event_manager_class()

    def register_client(self, name, client):
        self._clients[name] = client
        return client

    def register_service(self, service: Service):
        self._services[service.name] = service
        service.set_app(self)
        return service

    def register_view(self, view: View):
        self._views[view.name] = view
        view.set_app(self)
        return view

    def register_command(self, command: Command, events=None):
        self._commands[command.name] = command
        command.set_app(self)
        events = events or [command.__class__.__name__[:-len('Command')]]
        for event in events:
            self._event_manager.subscribe(event, command)
        return command

    def notify(self, notification):
        return self._event_manager.notify(notification)

    @property
    def clients(self):
        return self._clients

    @property
    def services(self):
        return self._services

    @property
    def views(self):
        return self._views

    @property
    def commands(self):
        return self._commands
