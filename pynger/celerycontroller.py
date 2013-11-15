# -*- coding: utf-8 -*-
""" A controller to rule over Celery. """

import locale
import os
import signal
import subprocess
import time
# local
from .config import PYNGER_PIDFILE, LOG


class CeleryController(object):

    def __init__(self):
        self.pid = self.find_pid()


    def start(self):
        LOG.debug('starting celery...')
        commands = ('celery', '-A', 'pynger.tasks', 'worker',# '--detach'
                    '--loglevel=DEBUG', '--pidfile=' + PYNGER_PIDFILE, '--beat')
        subprocess.call(commands)
        LOG.debug('done!')


    def stop(self):
        LOG.debug('stopping celery...')
        try:
            os.kill(int(self.pid), signal.SIGTERM)
            LOG.debug('done!')
        except:
            LOG.debug("Not running, nothing to stop...")
        self.remove_pidfile()


    def restart(self):
        self.stop()
        time.sleep(2)
        self.start()


    def remove_pidfile(self):
        try:
            os.remove(PYNGER_PIDFILE)
        except:
            pass


    def find_pid(self):
        self.pid = None
        try:
            with open(PYNGER_PIDFILE, 'r') as pidfile:
                self.pid = pidfile.readline().strip()
                LOG.debug("PID is: " + self.pid)
        except:
            LOG.debug("PID file does not exists")

        return(self.pid)


    def running_celerys(self):
        """ Works well on a Debian, didn't check other OS. """
        ps = subprocess.Popen(('ps', 'x'), stdout=subprocess.PIPE)
        output = ps.communicate()[0]
        processes = []
        pid = None
        for line in output.decode(locale.getdefaultlocale()[1]).split('\n'):
            if PYNGER_PIDFILE in line:
                first_space = line.find(' ')
                processes.append(line[:first_space])

        if len(processes) > 1:
            LOG.warning("You have more than one celery process, this is not good...")
        return(processes)


    def set_config(self):
        pass

