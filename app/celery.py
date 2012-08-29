from __future__ import absolute_import

from celery import Celery
from datetime import timedelta
from os import environ

redis_url = environ.get('REDISTOGO_URL', 'redis://localhost')
celery = Celery(broker=redis_url,
                include=['pit.tasks'])

CELERYBEAT_SCHEDULE = {
    'Get latest packages every five minutes': {
        'task': 'package.get_latest_packages',
        'schedule': timedelta(seconds=300),
    },
}

celery.conf.update(
    CELERYD_CONCURRENCY=10,
    CELERYD_MAX_TASKS_PER_CHILD=100,
    CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE,
)


from package.tasks import *
from pit.tasks import *
