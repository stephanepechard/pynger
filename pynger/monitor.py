# -*- coding: utf-8 -*-
""" A monitor is used to send requests. """

# system
from datetime import timedelta
# pipped
import requests


#class Monitor(object):


class HttpStatusMonitor(object):

    def execute(self, url):
        status = True
        try:
            req = requests.head(url, allow_redirects=True)
            status = req.status_code == 200
        except requests.exceptions.ConnectionError:
            status = False

        return(status)
