# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0005_auto_20150901_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='donation',
            name='charge_id',
            field=models.CharField(help_text=b'The charge ID from Stripe.', max_length=100, verbose_name=b'Charge ID', blank=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
