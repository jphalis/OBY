from __future__ import absolute_import

import os
import django

from django.conf import settings

from celery import Celery
from celery.utils.log import get_task_logger


# logger = get_task_logger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oby.settings')

django.setup()

app = Celery('oby')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @app.task
# def post_created(user):
#     "Executed on a post creation"
#     logger.info("post created")
# 
# 
# Views - post_created.delay()


# @app.task
# def call_command(name, *args, **kwargs):
#     "Calls a django command in a delayed fashion"
#     logger.info("calling django command %s with %s and %s" % (name, args, kwargs))
#     from django.core.management import call_command
#     call_command(name, *args, **kwargs)


# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
