# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='order_id',
            new_name='donation_id',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='status',
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.DecimalField(default=0.0, max_digits=30, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='donation',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
