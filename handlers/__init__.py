# -*- coding:utf-8 -*-

import inspect

from sanic import Blueprint


def import_all():
    from . import statistics
    from . import html
    return locals().values()


def import_all_blueprint(whitelist=None):
    modules = import_all()
    blueprints = {}

    for module in modules:
        for name, value in inspect.getmembers(module, lambda attr: isinstance(attr, Blueprint)):
            if name in blueprints:
                raise RuntimeError("duplicate blueprint name: %s, %s, %s" % (name, repr(value), repr(blueprints[name])))
            if not whitelist or name in whitelist:
                blueprints[name] = value

    return blueprints
