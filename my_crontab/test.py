# -*- coding:utf-8 -*-

from sanic.log import logger
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def test_scheduler():
    logger.info("test_scheduler")

# async task 有问题
# async def async_test():
#     logger.info("async_test")


scheduler.add_job(test_scheduler, 'cron', second=5)
# scheduler.add_job(async_test(), 'interval', seconds=10)
