# from __future__ import absolute_import
# from celery import shared_task
# from celery.decorators import periodic_task
# from celery.task.schedules import crontab

# from .celery import app


# # A periodic task that will run every minute (the symbol "*" means every)
# # @periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))


# @shared_task
# def add(x, y):
#     return x + y


# @shared_task
# def mul(x, y):
#     return x * y


# @shared_task
# def xsum(numbers):
#     return sum(numbers)


# @app.task
# def hello_world():
#     print ("Hello world")
