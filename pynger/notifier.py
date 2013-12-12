# -*- coding: utf-8 -*-
""" A notifier send information to users. """

# system
from datetime import timedelta
from email.mime.text import MIMEText
import smtplib
# pipped
import requests


class Notifier(object):

    address = None
    text = None

    def send(self):
        pass


class MailNotifier(Notifier):

    def send(self):

        msg = MIMEText(self.text, 'plain')
        msg['Subject'] = '[Pynger] Failure notification'
        msg['From'] = 's13d@free.fr'
        msg['To'] = self.address

        s = smtplib.SMTP('localhost')
        s.sendmail(msg['From'], [msg['To']], msg.as_string())
        s.quit()


class WebNotifier(Notifier):

    def send(self):
        pass
