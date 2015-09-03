# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0007_auto_20150901_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='message',
            field=models.TextField(max_length=4000, blank=True),
        ),
    ]
