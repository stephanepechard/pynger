# -*- coding: utf-8 -*-
""" A monitor is used to send requests. """

# system
from datetime import timedelta
# pipped
import requests


class Monitor(object):

    def __init__(self):
        self.mon_type = None

    def run(self):
        pass



class HttpStatusMonitor(Monitor):

    def __init__(self, url, freq=1):
        self.url = url
        self.freq = freq

    def create_task(self):
        return({self.url: {'task': 'pyng.monitor.run',
                           'schedule': timedelta(minutes=self.freq)},
                           'args': (self.url)
                          })

    def run(self):
        req = requests.get(self.url)
        success = req.status_code == 200
        print(success)
        return(success)

        # in case of failure, look at celery retry capabilities
