# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-created']},
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='timestamp',
            new_name='created',
        ),
    ]
