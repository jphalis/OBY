# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_auto_20150831_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='pageview',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 11, 4, 6, 291397), auto_now=True),
            preserve_default=False,
        ),
    ]
