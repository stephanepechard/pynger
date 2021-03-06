# -*- coding: utf-8 -*-

from .pynger import DotfileReader
reader = DotfileReader()

CELERYBEAT_SCHEDULE = reader.extract_tasks()
BROKER_URL = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'Europe/Paris'
