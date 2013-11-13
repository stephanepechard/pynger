# -*- coding: utf-8 -*-

from celery import task

@task
def run():
    with open('/tmp/celery.task', 'a') as celeryfile:
        celeryfile.write('task\n')

    mon = HttpStatusMonitor('http://google.com/')
    mon_task = mon.create_task()
    mon.run()
