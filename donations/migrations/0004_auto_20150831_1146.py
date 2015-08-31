# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0003_auto_20150831_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='message',
            field=models.CharField(default='', max_length=4000, blank=True),
            preserve_default=False,
        ),
    ]
