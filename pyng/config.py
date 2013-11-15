# -*- coding: utf-8 -*-

# system
import os

# pid file of the child process
PYNG_PIDFILE = os.path.join(os.environ['HOME'], '.pyng.pid')
# default log file
PYNG_LOGFILE = os.path.join(os.environ['HOME'], '.pyng.log')
# default config file
PYNG_DOTFILE = os.path.join(os.environ['HOME'], '.pyng.json')
# time multipliers
TIME_MULTIPLIERS = {'s': 1, 'm': 60, 'h': 60*60, 'd': 60*60*24}


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
        'pyng': {
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
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler(PYNG_LOGFILE, 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
LOG.addHandler(file_handler)
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
LOG.addHandler(steam_handler)
