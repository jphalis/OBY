# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_auto_20150831_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 11, 6, 4, 284615), auto_now=True),
            preserve_default=False,
        ),
    ]
