# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_auto_20150826_2216'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['created']},
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='updated',
            new_name='modified',
        ),
    ]
