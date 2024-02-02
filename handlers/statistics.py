# -*- coding:utf-8 -*-

from sanic import Blueprint
from sanic import response
from sanic.log import logger

from util.rpc_decorator import rpc_method, Int, Str, List, Dict, Any

static = Blueprint('static', url_prefix='/static')


@static.route('/SpurLineEntity', methods=["POST"])
@rpc_method(Str(), Int())
async def SpurLineEntity(request, name, server):
    collection = request.app.ctx.mongodb["test"]
    info = {
        "name": name,
        "server": server,
    }
    # collection.insert_one(info)
    return response.json({"suc": 1})
