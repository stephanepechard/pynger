# -*- coding: utf-8 -*-

# system
import pprint
# pipped
from celery import Celery
# local
from .config import FAILURE, SUCCESS, MONITORS_TYPE, NOTIFIERS_TYPE, LOG, \
    HISTORY, PYNGER_HISFILE, SEPARATOR
from .pynger import DotfileReader


# celery
celery = Celery('pynger.tasks')
celery.config_from_object('pynger.celeryconfig')

# history
reader = DotfileReader()


@celery.task
def notify(name, url):

    send = False
    # determine if we need to send a notification
    with open(PYNGER_HISFILE, 'r') as hisfile:
        for line in hisfile.readlines():
            items = dict(zip(['datetime', 'name', 'mtype', 'status'],
                             line.rstrip('\n').split(SEPARATOR)))
            if name == items['name']:
                # only the last one is taken into account
                send = items['status'] != SUCCESS

    # send it
    if send:
        notifiers = reader.extract_notifiers(name)
        for notif in notifiers:
            notifier = NOTIFIERS_TYPE[notif['type']]()
            notifier.address = notif['address']
            notifier.text = "Hello,\nThe site {} seems down, check it out!".format(url)
            notifier.send()


@celery.task
def monitor(name, url, mtype):
    mon = MONITORS_TYPE[mtype]()
    success = mon.execute(url)
    LOG.debug("pynging {}: {}".format(url, SUCCESS if success else FAILURE))
    HISTORY.info(SEPARATOR.join([name, mtype, SUCCESS if success else FAILURE]))

    if not success:
        notify.delay(name, url)
