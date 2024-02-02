# -*- coding:utf-8 -*-

import json
import sys

from functools import wraps

from sanic import response
from sanic.log import logger


class RpcMethodArg(object):
    """
    RPC参数的基类。
    """
    TYPE = None

    def __init__(self, default=None) -> None:
        super(RpcMethodArg, self).__init__()
        self._default = default

    def get_type(self):
        return self.__class__.__name__

    def do_convert(self, data):
        try:
            return self.convert(data)
        except:
            raise self.convert_error(data)

    def convert(self, data):
        if isinstance(data, self.TYPE):
            return data
        return self.TYPE(data)

    def convert_error(self, data):
        return ValueError("Cannot Data [%r] To Type [%s]." % (data, self.get_type()))

    def get_default(self):
        raise ValueError("Not implemented!")

    @property
    def default(self):
        if self._default is not None:
            return self._default
        return self.get_default()


class Int(RpcMethodArg):
    """int 型参数。"""
    TYPE = int

    def get_default(self):
        return 0


class Float(RpcMethodArg):
    """float型参数。"""
    TYPE = float

    def get_default(self):
        return 0


class Str(RpcMethodArg):
    """str型参数。"""
    TYPE = str

    def get_default(self):
        return ""


class List(RpcMethodArg):
    """list型参数。"""
    TYPE = list

    def get_default(self):
        return []


class Dict(RpcMethodArg):
    """dict型参数。"""
    TYPE = dict

    def get_default(self):
        return {}


class Bool(RpcMethodArg):
    """bool型参数。"""
    TYPE = bool

    def convert(self, data):
        try:
            return bool(data)
        except:
            raise self.convert_error(data)

    def get_default(self):
        return False


class Any(RpcMethodArg):

    def convert(self, data):
        return data

    def get_type(self):
        return self.__class__.__name__


def rpc_method(*types):
    def _rpc_method(func):
        argcount = func.__code__.co_argcount
        argnames = func.__code__.co_varnames
        len_types = len(types)

        argtypes = {}
        for argindex in range(1, argcount):
            argname = argnames[argindex]
            if argindex <= len_types:
                argtype = types[argindex - 1]
            else:
                argtype = Any()
            argtypes[argname] = argtype
        func.argtypes = argtypes

        @wraps(func)
        def _rpc_method_xargs(request, *args):
            try:
                params = {}
                if request.method == "POST":
                    params = json.loads(request.body)
                else:
                    request_args = request.args
                    for k, values in request_args.items():
                        if len(values) != 1:
                            raise RuntimeError("Request Args Extract Failure")
                        params[k] = values[0]

                params.pop("_", None)
                logger.info("%s %s %s", request.method, request.url, params)

                args = {}
                for key, decorator_type in func.argtypes.items():
                    if key in params:
                        args[key] = decorator_type.do_convert(params[key])
                        params[key] = decorator_type.do_convert(params[key])
                    else:
                        args[key] = decorator_type.default
                        params[key] = decorator_type.default

                # if len(func.argtypes) == 1 and isinstance(list(func.argtypes.values())[0], Dict):
                #     return func(request, params)

                if func.__code__.co_flags & 8:  # (**kawargs)
                    return func(request, **params)
                else:
                    return func(request, **args)

            except:
                sys.excepthook(*sys.exc_info())
                return response.json("Request: %s. %s\n" % (request.url, sys.exc_info()), status=400)

        return _rpc_method_xargs

    return _rpc_method
