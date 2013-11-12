# -*- coding: utf-8 -*-
""" A controller to rule over Celery. """

import subprocess
from subprocess import Popen, PIPE
import time
# local
from pyng.config import PYNG_PIDFILE, LOG

# see https://github.com/celery/celery/blob/9c00d0c67c0844e4b62d60839c55a79c64666c93/extra/generic-init.d/celerybeat
class CeleryController(object):

    def __init__(self):
        self.pid = None


    def start(self):
        LOG.info('starting celery...')
        commands = ('./venv/local/bin/celery', 'beat', '--detach',
                    '--pidfile=' + PYNG_PIDFILE, '--config=pyng.celeryconfig')
        subprocess.call(commands)
        LOG.info('done!')


    def reload_celery(self):
        self.stop()
        time.sleep(2)
        self.start()


    def stop_celery(self):
        self.reload_pid()
        LOG.info('stopping celery...')
        LOG.info('done')


    def reload_pid(self):
        self.pid = None
        try:
            with open(PYNG_PIDFILE, 'r') as pidfile:
                self.pid = pidfile.readline()
                LOG.info("PID is: " + self.pid)
        except FileNotFoundError:
            LOG.warning("PID file does not exists")

