BROKER_URL = 'redis://localhost:6379/0'

from datetime import timedelta
CELERYBEAT_SCHEDULE = {
    'monitorize-every-10-seconds': {
        'task': 'pyng.tasks.monitorize',
        'schedule': timedelta(seconds=10),
        'args': ['http://msn.com/'],
    },
}
