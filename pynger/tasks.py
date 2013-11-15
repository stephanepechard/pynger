# -*- coding: utf-8 -*-

# pipped
from celery import Celery
# local
from .config import MONITORS_TYPE, LOG


# celery
celery = Celery('pynger.tasks')
celery.config_from_object('pynger.celeryconfig')


@celery.task
def monitor(url, mtype):
    mon = MONITORS_TYPE[mtype]()
    success = mon.execute(url)
    LOG.info("pynging {}: {}".format(url, "SUCCESS" if success else "FAILURE"))