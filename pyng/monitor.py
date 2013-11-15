# -*- coding: utf-8 -*-
""" A monitor is used to send requests. """

# system
from datetime import timedelta
# pipped
import requests


#class Monitor(object):


class HttpStatusMonitor(object):

    def execute(self, url):
        req = requests.head(url, allow_redirects=True)
        return(req.status_code == 200)

        # in case of failure, look at celery retry capabilities
