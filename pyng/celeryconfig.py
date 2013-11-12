# Absolute or relative path to the 'celery' command:
CELERY_BIN="../venv/local/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="pyng"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# Where to chdir at start.
CELERYBEAT_CHDIR="../"

# Extra arguments to celerybeat
#CELERYBEAT_OPTS="--schedule=/var/run/celerybeat-schedule"

BROKER_URL = 'redis://localhost:6379/0'
