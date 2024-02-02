# -*- coding:utf-8 -*-

import asyncio

from pymongo import MongoClient


def mongo_init(app):
    config = app.config["MONGO_CONFIG"]
    client = MongoClient(**config)
    data_base = app.config["MONGO_DATABASE"]
    db = client[data_base]
    app.ctx.mongodb = db
