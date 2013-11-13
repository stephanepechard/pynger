# -*- coding: utf-8 -*-
""" A controller to rule over Celery. """

import locale
import os
import re
import signal
import subprocess
import sys
import time
# pipped
import sh
# local
from pyng.config import PYNG_PIDFILE, LOG


class CeleryController(object):

    def __init__(self):
        self.running = False
        self.pid = self.find_pid()


    def start(self):
        LOG.info('starting celery...')
        commands = ('./venv/local/bin/celery', 'beat',# '--detach',
                    '--loglevel=DEBUG',
                    '--pidfile=' + PYNG_PIDFILE, '--config=pyng.celeryconfig')
        subprocess.call(commands)
        self.running = True
        LOG.info('done!')


    def stop(self):
        if self.running:
            LOG.info('stopping celery...')
            os.kill(int(self.pid), signal.SIGTERM)
            self.running = False
            LOG.info('done!')
        else:
            sys.exit("Not running, nothing to stop...")


    def restart(self):
        self.stop()
        time.sleep(2)
        self.start()


    def find_pid(self):
        self.pid = None
        try:
            with open(PYNG_PIDFILE, 'r') as pidfile:
                self.pid = pidfile.readline().strip()
                self.running = True
                LOG.info("PID is: " + self.pid)
        except FileNotFoundError:
            LOG.info("PID file does not exists")
            self.running = False

        return(self.pid)


    def running_celerys(self):
        """ Works well on a Debian, didn't check other OS. """
        ps = subprocess.Popen(('ps', 'x'), stdout=subprocess.PIPE)
        output = ps.communicate()[0]
        processes = []
        pid = None
        for line in output.decode(locale.getdefaultlocale()[1]).split('\n'):
            if PYNG_PIDFILE in line:
                first_space = line.find(' ')
                processes.append(line[:first_space])

        if len(processes) > 1:
            LOG.warning("You have more than one celery process, this is not good...")
        return(processes)


    def set_config(self):
        pass



