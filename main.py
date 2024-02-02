# -*- coding:utf-8 -*-
import asyncio

from sanic import Sanic
from sanic import response, text
from sanic.log import logger

import handlers
import my_crontab
from util.sanic_config import CONFIG
from util.sanic_mongo import mongo_init
from sanic.log import logger


app = Sanic("XHSanic")
app.config.update(CONFIG)

mongo_init(app)

blueprints = handlers.import_all_blueprint()
logger.info("import_all_blueprint total %s detail: %s", len(blueprints), blueprints)
for name, blueprint in blueprints.items():
    app.blueprint(blueprint)


@app.main_process_start
async def main_start(*_):
    logger.info(">>>>>> main_start <<<<<<")


@app.before_server_start
async def setup_db(app):
    logger.info(">>>>>> before_server_start <<<<<<")


@app.get('/')
async def hello(request):
    return text("OK!")


my_crontab.start_all_crontab()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=16471, debug=False, access_log=True, workers=2)
