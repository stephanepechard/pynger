# -*- coding: utf-8 -*-

# logging setup
import logging
from logging.handlers import RotatingFileHandler
LOG = logging.getLogger()
LOG.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('/tmp/pyng.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
LOG.addHandler(file_handler)
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
LOG.addHandler(steam_handler)


# pid file of the child process
PYNG_PIDFILE = '/tmp/pyng.pid'




