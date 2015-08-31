# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_follower_modified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='updated',
            new_name='modified',
        ),
    ]
