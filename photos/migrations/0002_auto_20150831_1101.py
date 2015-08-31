# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['-created']},
        ),
        migrations.RenameField(
            model_name='photo',
            old_name='timestamp',
            new_name='created',
        ),
    ]
