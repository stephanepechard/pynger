# -*- coding: utf-8 -*-

# pipped
from celery import Celery
# local
from pyng.monitor import HttpStatusMonitor


# celery
celery = Celery('pyng.tasks')
celery.config_from_object('pyng.celeryconfig')


@celery.task
def monitorize(url):
    mon = HttpStatusMonitor(url)
    mon_task = mon.create_task()
    mon.execute()
