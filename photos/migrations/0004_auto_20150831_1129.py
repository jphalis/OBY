# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0003_photo_modified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='timestamp',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='updated',
            new_name='modified',
        ),
    ]
