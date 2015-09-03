# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20150902_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='stripe_customer_id',
            field=models.CharField(max_length=30, editable=False, blank=True),
        ),
    ]
