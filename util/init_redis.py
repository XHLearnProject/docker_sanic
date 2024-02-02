# -*- coding:utf-8 -*-

from sanic.log import logger

from aredis import StrictRedisCluster
from aredis import ClusterConnectionPool

REDIS_CONFIG = {
    "startup_nodes": [
        {'host': '10.216.109.125', 'port': 9736},
        {'host': '10.216.109.123', 'port': 9736},
    ],
    "password": "123456",
    "max_connections": 500,
}


async def async_aio_redis_init(app):
    redis_pool = ClusterConnectionPool(**REDIS_CONFIG)
    redis_poll_conn = StrictRedisCluster(connection_pool=redis_pool)
    await redis_poll_conn.ping()
    app.ctx.redis = redis_poll_conn
    logger.info("init redis done! %s", redis_poll_conn)


def aio_redis_cluster_init(app):
    app.add_task(async_aio_redis_init(app))
