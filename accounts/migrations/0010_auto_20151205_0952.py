# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20151127_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='gender',
            field=models.CharField(blank=True, max_length=6, choices=[(b'DUDE', 'Dude'), (b'BETTY', 'Betty')]),
        ),
    ]
