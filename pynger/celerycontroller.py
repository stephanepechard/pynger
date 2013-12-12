# -*- coding: utf-8 -*-
""" A controller to rule over Celery. """

import locale
import os
import signal
import subprocess
import time
# local
from .config import PYNGER_PIDFILE, PYNGER_CELERYLOGFILE, LOG


class CeleryController(object):

    def __init__(self):
        self.pid = self.find_pid()


    def start(self):
        LOG.debug('starting celery...')
        commands = ('celery', '-A', 'pynger.tasks', 'worker', '--detach',
                    '--loglevel=INFO', '--pidfile=' + PYNGER_PIDFILE, 
                    '--logfile=' + PYNGER_CELERYLOGFILE, '--beat')
        subprocess.call(commands)
        LOG.debug('Pynger has started')


    def stop(self):
        LOG.debug('stopping celery...')
        try:
            os.kill(int(self.pid), signal.SIGTERM)
            LOG.debug('Pynger has stopped')
        except:
            LOG.debug("Not running, nothing to stop...")
        self.remove_pidfile()


    def restart(self):
        self.stop()
        self.kill_all()
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
        for sline in output.decode(locale.getdefaultlocale()[1]).split('\n'):
            line = sline.strip()
            if PYNGER_PIDFILE in line:
                first_space = line.find(' ')
                processes.append(line[:first_space])

        if len(processes) > 1:
            # look at how many workers are launched before warning!
            LOG.warning("You have more than one celery process, this is not good...")
            LOG.warning("Processes are: {}".format(processes))
        return(processes)


    def kill_all(self):
        for proc in self.running_celerys():
            os.kill(int(proc), signal.SIGTERM)
            LOG.warning("Killing process " + proc)

