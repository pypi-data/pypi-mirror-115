import inspect
from collections import OrderedDict
from functools import wraps
from inspect import signature

from csengine.extentions.fastapi.view import events
from csengine.view import View
from fastapi import APIRouter, File, Form, UploadFile, Body, Request, HTTPException


def action(method, *args, forms=None, files=None, body=None, roles=None,
           serializer_class=None, **kwargs):

    def decorator(funct):
        funct.action_name = funct.__name__
        funct.action_method = method
        funct.action_forms = forms or []
        funct.action_files = files or []
        funct.action_body = body or []
        funct.action_args = args
        funct.action_kwargs = kwargs
        funct.roles = roles or []
        funct.serializer_class = serializer_class
        return funct

    return decorator


def post(*args, **kwargs):
    return action("post", *args, **kwargs)


def get(*args, **kwargs):
    return action("get", *args, **kwargs)


def put(*args, **kwargs):
    return action("put", *args, **kwargs)


def delete(*args, **kwargs):
    return action("delete", *args, **kwargs)


class FastAPIView(View):
    router_class = APIRouter
    roles = []
    request_class = Request

    def __init__(self, name=None, app=None):
        super().__init__(name, app)

    @classmethod
    def get_actions(cls):
        members = inspect.getmembers(cls, inspect.isfunction)
        return {name: action for name, action in members
                if hasattr(action, 'action_name')}

    def get_router(self):
        router = self.router_class()

        for action_name, action in self.get_actions().items():
            args = action.action_args
            kwargs = action.action_kwargs
            wrapper = self.wrap_action(action)
            wrapper = self._run_preprocessing(wrapper)
            getattr(router, action.action_method)(*args, **kwargs)(wrapper)

        return router

    def _run_preprocessing(self, action):
        sig = signature(action)
        params = OrderedDict(sig.parameters.items())
        serializer_class = action.serializer_class
        forms = action.action_forms
        files = action.action_files
        body = action.action_body

        if serializer_class:
            params.update(serializer_class.__signature__.parameters)
            forms += getattr(serializer_class.Meta, 'forms', [])
            body += getattr(serializer_class.Meta, 'body', [])
            files += getattr(serializer_class.Meta, 'files', [])

        self.prepare_params(params, files=files, forms=forms, body=body)
        sig = sig.replace(parameters=tuple(params.values()))
        action.__signature__ = sig

        return action

    def prepare_params(self, params, files, forms, body):
        for name, value in params.items():
            annotation_cls = self._get_annotation_class(value.annotation)
            if ((issubclass(annotation_cls, UploadFile)
                 or issubclass(annotation_cls, bytes))
                    and (value.default is value.empty)):
                files.append(name)

        for name, value in params.items():
            if name in files and value.default is value.empty:
                value = value.replace(default=File(...))
            elif name in forms and value.default is value.empty:
                value = value.replace(default=Form(...))
            elif name in forms and not isinstance(value.default, Form.__class__):
                value = value.replace(default=Form(default=value.default))
            elif name in body and value.default is value.empty:
                value = value.replace(default=Body(..., embed=True))
            elif name in body and not isinstance(value.default, Body.__class__):
                value = value.replace(default=Body(default=value.default, embed=True))

            params[name] = value

        return params

    def wrap_action(self, action):
        # action_sig = signature(action)
        # parameters = [parameter for parameter in action_sig.parameters.values()
        #               if parameter.annotation == Request]
        # request_parameter = parameters[0] if parameters else \
        #     Parameter('request', Parameter.POSITIONAL_OR_KEYWORD, annotation=Request)

        @wraps(action)
        async def wrapper(request: Request, *args, **kwargs):
            request.scope['action'] = action
            return await self.run_action(action, request, args, kwargs)

        # Override signature
        sig = signature(wrapper)
        # params = [Parameter('_request', Parameter.POSITIONAL_OR_KEYWORD, annotation=Request)]
        # params += list(sig.parameters.values())[1:]
        params = list(sig.parameters.values())[1:]
        sig = sig.replace(parameters=tuple(params))
        wrapper.__signature__ = sig

        return wrapper

    def _get_annotation_class(self, annotation):
        return annotation if type(annotation) == type else annotation.__class__

    async def run_action(self, action, request, args, kwargs):
        await self.app.notify(events.ActionStartedEvent(action, request, args, kwargs))
        if not await self.auth(action, request, args, kwargs):
            raise HTTPException(status_code=401)
        await self.validate(action, request, args, kwargs)
        return await action(self, request, *args, **kwargs)

    async def validate(self, action, request, args, kwargs):
        if action.serializer_class:
            request.scope['serializer'] = action.serializer_class(view=self, **kwargs)
            await request.scope['serializer'].validate_data()

    async def auth(self, action, request, args, kwargs):
        roles = action.roles or self.roles
        if not roles:
            return True
        user_roles = request.scope.get('user_roles', {})
        return set(roles) & set(user_roles)
