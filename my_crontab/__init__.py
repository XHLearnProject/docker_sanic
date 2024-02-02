# -*- coding:utf-8 -*-
import inspect

from apscheduler.schedulers.base import BaseScheduler


def import_all():
    from . import test
    return locals().values()


def get_all_crontab():
    crontab_list = []
    for module in import_all():
        for name, scheduler in inspect.getmembers(module, lambda obj: isinstance(obj, BaseScheduler)):
            print('find crontab named %s in %s ' % (name, module))
            crontab_list.append(scheduler)
    return crontab_list


def start_all_crontab():
    for scheduler in get_all_crontab():
        scheduler.start()
