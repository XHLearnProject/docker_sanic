# -*- coding:utf-8 -*-

import os

from sanic import Blueprint
from sanic import response
from sanic.log import logger

from util.rpc_decorator import rpc_method, Int, Str, List, Dict, Any

html = Blueprint('html', url_prefix='/html')

@html.route('/<html>', methods=["GET"])
async def GetHTML(request, html):
    return await response.file(os.path.join('html', html))
