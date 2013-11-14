# -*- coding: utf-8 -*-
""" A controller to rule over Celery. """

import locale
import os
import signal
import subprocess
import time
# local
from .config import PYNG_PIDFILE, LOG


class CeleryController(object):

    def __init__(self):
        self.running = False
        self.pid = self.find_pid()


    def start(self):
        LOG.debug('starting celery...')
        commands = ('celery', '-A', 'pyng.tasks', 'worker',# '--detach'
                    '--loglevel=DEBUG', '--pidfile=' + PYNG_PIDFILE, '--beat')
        subprocess.call(commands)
        self.running = True
        LOG.debug('done!')


    def stop(self):
        LOG.debug('stopping celery...')
        try:
            os.kill(int(self.pid), signal.SIGTERM)
            LOG.debug('done!')
        except:
            LOG.debug("Not running, nothing to stop...")
        self.running = False
        self.remove_pidfile()


    def restart(self):
        self.stop()
        time.sleep(2)
        self.start()


    def remove_pidfile(self):
        try:
            os.remove(PYNG_PIDFILE)
        except:
            pass


    def find_pid(self):
        self.pid = None
        try:
            with open(PYNG_PIDFILE, 'r') as pidfile:
                self.pid = pidfile.readline().strip()
                self.running = True
                LOG.debug("PID is: " + self.pid)
        except:
            LOG.debug("PID file does not exists")
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

