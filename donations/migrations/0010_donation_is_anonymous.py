# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0009_auto_20150903_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='is_anonymous',
            field=models.BooleanField(default=True),
        ),
    ]
