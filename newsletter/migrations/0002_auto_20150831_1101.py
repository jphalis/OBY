# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsletter',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='newsletter',
            old_name='updated',
            new_name='modified',
        ),
    ]
