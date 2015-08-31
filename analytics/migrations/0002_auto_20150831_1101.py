# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pageview',
            options={'ordering': ['-created']},
        ),
        migrations.RenameField(
            model_name='pageview',
            old_name='timestamp',
            new_name='created',
        ),
    ]
