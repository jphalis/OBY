# from __future__ import absolute_import
# from celery import shared_task
from celery.decorators import periodic_task, task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger

# from .celery import app


logger = get_task_logger(__name__)


# A periodic task that will run every minute (the symbol "*" means every)
# "*/15" == every fifteen mintues
# @periodic_task(run_every=(crontab(hour="*", minute="*/15", day_of_week="*")),
#                name="some_task", ignore_result=True)
# def some_task():
#     # do something
#     pass


@task(name="sum_two_numbers")
def add(x, y):
    return x + y

# useage:
# add.delay(7, 8)


# @shared_task
# def mul(x, y):
#     return x * y


# @shared_task
# def xsum(numbers):
#     return sum(numbers)


# @app.task
# def hello_world():
#     print ("Hello world")
