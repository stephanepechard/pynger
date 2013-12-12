# -*- coding: utf-8 -*-

# system
import os

# pid file of the child process
PYNGER_PIDFILE = os.path.join(os.environ['HOME'], '.pynger.pid')
# default log file
PYNGER_LOGFILE = os.path.join(os.environ['HOME'], '.pynger.log')
# default log file
PYNGER_HISFILE = os.path.join(os.environ['HOME'], '.pynger.history')
# default celery log file
PYNGER_CELERYLOGFILE = '/tmp/pynger-celery.log'
# default config file
PYNGER_DOTFILE = os.path.join(os.environ['HOME'], '.pynger.json')
# time multipliers
TIME_MULTIPLIERS = {'s': 1, 'm': 60, 'h': 60*60, 'd': 60*60*24}
# status code
SUCCESS = "fr.s13d.pynger.SUCCESS"
FAILURE = "fr.s13d.pynger.FAILURE"
# separator
SEPARATOR = ';'

# monitors type
from .monitor import HttpStatusMonitor
MONITORS_TYPE = {
    "http-status": HttpStatusMonitor,
}
from .notifier import MailNotifier, WebNotifier
NOTIFIERS_TYPE = {
    "mail": MailNotifier,
    "web": WebNotifier,
}


# dotfile official schema
DOTFILE_SCHEMA = {
    'type' : "object",
    'properties' : {
        'pynger': {
            'type' : "array",
            'items': {
                'type': 'object',
                'properties': {
                    "name": { "type" : "string" },
                    'monitors': {
                        'type' : "array",
                        'items': {
                            'type': 'object',
                            'properties': {
                                "type": { "type" : "string" },
                                "url":  { "type" : "string" },
                                "freq": { "type" : "string" },
                            }
                        }
                    },
                    'notifiers': {
                        'type' : "array",
                        'items': {
                            'type': 'object',
                            'properties': {
                                "type": { "type" : "string" },
                                "address": { "type" : "string" },
                            }
                        }
                    },
                }
            }
        }
    }
}


# logging setup
import logging
from logging.handlers import RotatingFileHandler
LOG = logging.getLogger("pynger")
LOG.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler(PYNGER_LOGFILE, 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
LOG.addHandler(file_handler)
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
LOG.addHandler(steam_handler)


# history setup
import logging
from logging.handlers import RotatingFileHandler
HISTORY = logging.getLogger("pynger-history")
HISTORY.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s{}%(message)s'.format(SEPARATOR))
file_handler = RotatingFileHandler(PYNGER_HISFILE, 'a', 1000000, 1)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
HISTORY.addHandler(file_handler)

