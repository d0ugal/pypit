from __future__ import absolute_import

from celery import Celery

celery = Celery(broker='redis://localhost',
                include=['pit.tasks'])

celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)
