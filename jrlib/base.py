import json
import logging
import re
import sys
from collections import OrderedDict, defaultdict
from importlib import import_module
import traceback
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .fields import UNDEF, BaseField

api_methods = {}

# TODO: move from global namespace or clean each time by run api method
order_middles = defaultdict(list)
middle_order = {}
fields_middles_map = defaultdict(list)

DEBUG = settings.DEBUG
JR_API_DIR = settings.JR_API_DIR
JR_API_FILE = settings.JR_API_FILE

# TODO: remove from global namespace after testing ordered middleware
middles_is_mapped_to_fields = []
last_middles = []


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
        cls._fields = {key: val.order for key, val in namespace.items()
                       if isinstance(val, BaseField)}
        # form inheritance
        for item in cls_mro[1:-1]:  # exclude UserCustomMethod and object
            if hasattr(item, '_fields'):
                cls._fields.update(item._fields)
        cls._fields = OrderedDict(
            sorted(cls._fields.items(), key=lambda item: item[1]))
        return cls


class Method(metaclass=MetaBase):

    def __init__(self, request, data, *args, **kwargs):
        print('class method init')
        self.request = request
        self.result = UNDEF
        print('M F {}'.format(self._fields))
        fields = list(self._fields.items())
        # middles_is_mapped_to_fields = []
        # TODO: run middleware before all if order_middle less then order first field
        # if fields:
        #     prev_field = fields[0]
        #     for item_field in fields[1:]:
        #         for order, middles in order_middles.items():
        #             for middle in middles:
        #                 if middle not in middles_is_mapped_to_fields:
        #                     if order < item_field[1]:
        #                         fields_middles_map[prev_field[0]].append(
        #                             middle)
        #                         middles_is_mapped_to_fields.append(middle)
        #         prev_field = item_field
        if fields:
            middle_methods_mro = {}
            for item in type(self).mro()[:-1]:
                middle_method = getattr(
                    self, '_{}__middle'.format(item.__name__), None)
                if middle_method:
                    orig_qualname = '{}.__middle'.format(item.__name__)
                    print('???????', orig_qualname)
                    # middle_methods_mro.append(middle_method)
                    middle_methods_mro[orig_qualname] = middle_method
            prev_field = fields[0]
            print('middle_order', middle_order)
            for item_field in fields[1:]:
                for orig_qualname, method in middle_methods_mro.items():
                    print('!!!!!!!', orig_qualname)
                    order = middle_order.get(orig_qualname)
                    if method not in middles_is_mapped_to_fields:
                        if order is not None and order < item_field[1]:
                            fields_middles_map[prev_field[0]].append(
                                method)
                            middles_is_mapped_to_fields.append(method)
                prev_field = item_field
        for key in self._fields:
            try:
                print('METHOD - {} : {}'.format(key, data.get(key)))
                setattr(self, key, data.get(key, UNDEF))
                # for ext validate (run validate_<field>)
                validator = getattr(self, 'validate_{}'.format(key), None)
                if validator:
                    validator(getattr(self, key))
                for middle_method in fields_middles_map[key]:
                    # middle_method(self)
                    middle_method()
            except Exception as exc:
                raise ValueError('{}: {}'.format(key, exc))
        self.validate()
        # for middleware (run __middle method)
        # TODO: run middleware that order_middle great then last field
        # TODO: run middleware if middleware not ordered by decorator
        for item in type(self).mro()[:-1]:
            middle_method = getattr(
                self, '_{}__middle'.format(item.__name__), None)
            if (middle_method and
                    middle_method not in middles_is_mapped_to_fields):
                middle_method()
                last_middles.append(middle_method)
        self.result = self.execute()
        # for middleware after execute (run __after method)
        for item in type(self).mro()[:-1]:
            after_method = getattr(
                self, '_{}__after'.format(item.__name__), None)
            if after_method:
                after_method()

    def validate(self):
        pass

    def execute(self):
        pass


def order(value):
    def decorator(func):
        order_middles[value].append(func)
        middle_order[func.__qualname__] = value

        def wrapper(*args, **kwargs):
            return_value = func(*args, **kwargs)
            return return_value

        return wrapper
    # print(id(decorator))
    return decorator
