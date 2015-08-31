# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0002_auto_20150830_1528'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donation',
            options={'ordering': ['-modified', '-created']},
        ),
        migrations.RenameField(
            model_name='donation',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='donation',
            old_name='updated',
            new_name='modified',
        ),
    ]
