import json
import logging
import re
import sys
from importlib import import_module
import traceback
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .fields import UNDEF, BaseField

api_methods = {}

DEBUG = settings.DEBUG
JR_API_DIR = settings.JR_API_DIR
JR_API_FILE = settings.JR_API_FILE


@csrf_exempt
def api_dispatch(request):
    try:
        body = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({'jsonrpc': '2.0',
                             'id': None,
                             'error': {'code': -32700,
                                       'message': 'Parse error'}})
    request_id = body.get('id')
    version = body.get('jsonrpc')
    if version != '2.0':
        error_text = "JSONRPC protocol version MUST be exactly '2.0'"
        return JsonResponse({'jsonrpc': '2.0',
                             'id': request_id,
                             'error': {'code': -32600,
                                       'message': 'Invalid Request',
                                       'data': {'text': error_text}}})
    api_name = body.get('method')
    if not api_name:
        error_text =\
            'Method field MUST containing the name of the method to be invoked'
        return JsonResponse({'jsonrpc': '2.0',
                             'id': request_id,
                             'error': {'code': -32600,
                                       'message': 'Invalid Request',
                                       'data': {'text': error_text}}})
    if api_name not in api_methods:
        try:
            # example: api.echo.method
            # file: api/echo/method.py
            import_module('{}.{}.{}'.format(JR_API_DIR, api_name, JR_API_FILE))
        except ModuleNotFoundError:
            return JsonResponse({'jsonrpc': '2.0',
                                 'id': request_id,
                                 'error': {'code': -32601,
                                           'message': 'Method not found'}})
        except Exception:
            jsonrpc_response = {'jsonrpc': '2.0', 'id': request_id}
            error = {'code': -1, 'message': 'Internal error'}
            stack = traceback.format_exc()
            if DEBUG:
                error['data'] = {
                    'stack': stack,
                    'executable': sys.executable}
            logging.error('{}'.format(stack))
            jsonrpc_response.update({'error': error})
            return JsonResponse(jsonrpc_response)
    cls = api_methods.get(api_name)
    if not cls:
        return JsonResponse({'jsonrpc': '2.0',
                             'id': request_id,
                             'error': {'code': -32601,
                                       'message': 'Method not found'}})
    params = body.get('params', {})  # TODO: support params as list (not {})
    jsonrpc_response = {'jsonrpc': '2.0', 'id': request_id}
    try:
        instance = cls(request, params)
        if instance.result is not UNDEF:
            jsonrpc_response.update({'result': instance.result})
        else:
            jsonrpc_response.update({'error': {'code': -32603,
                                               'message': 'Internal error'}})
    except Exception as exc:
        error = {'code': -1, 'message': str(exc)}
        stack = traceback.format_exc()
        if DEBUG:
            error['data'] = {
                'stack': stack,
                'executable': sys.executable}
        logging.error('{}'.format(stack))
        jsonrpc_response.update({'error': error})
    return JsonResponse(jsonrpc_response)


class MetaBase(type):
    def __new__(self, name, bases, namespace):
        cls = super(MetaBase, self).__new__(
            self, name, bases, namespace)
        cls_mro = cls.mro()
        if len(cls_mro) > 2:  # 1 - UserCustomMethod, 2 - Method, 3 - object
            api_name = cls.__name__
            api_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', api_name)
            api_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', api_name).lower()
            api_methods[api_name] = cls
        cls._fields = [key for key, val in namespace.items()
                       if isinstance(val, BaseField)]
        # form inheritance
        for item in cls_mro[1:-1]:  # exclude UserCustomMethod and object
            if hasattr(item, '_fields'):
                cls._fields.extend(item._fields)
        return cls


class Method(metaclass=MetaBase):

    def __init__(self, request, data, *args, **kwargs):
        print('class method init')
        self.request = request
        self.result = UNDEF
        print('M F {}'.format(self._fields))
        for key in self._fields:
            try:
                print('METHOD - {} : {}'.format(key, data.get(key)))
                setattr(self, key, data.get(key, UNDEF))
            except Exception as exc:
                raise ValueError('{}: {}'.format(key, exc))
        self.validate_fields()
        self.validate()
        # for middleware (run __middle method)
        for item in type(self).mro()[:-1]:
            middle_method = getattr(
                self, '_{}__middle'.format(item.__name__), None)
            if middle_method:
                middle_method()
        self.result = self.execute()
        # for middleware after execute (run __after method)
        for item in type(self).mro()[:-1]:
            after_method = getattr(
                self, '_{}__after'.format(item.__name__), None)
            if after_method:
                after_method()

    def validate_fields(self):
        for key in self._fields:
            validator = getattr(self, 'validate_{}'.format(key), None)
            if validator:
                try:
                    validator(getattr(self, key))
                except Exception as exc:
                    raise ValueError('{}: {}'.format(key, exc))

    def validate(self):
        pass

    def execute(self):
        pass

    def before(self):
        # TODO: вместо before будут декораторы, через которые можно навешивать валидаторы
        pass

    def after(self):
        # TODO: аналогично before
        pass
