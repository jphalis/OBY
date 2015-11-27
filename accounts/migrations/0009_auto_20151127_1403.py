# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_myuser_stripe_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='gender',
            field=models.CharField(blank=True, max_length=6, choices=[(b'dude', b'Dude'), (b'betty', b'Betty')]),
        ),
    ]
