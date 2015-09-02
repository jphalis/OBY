# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('donations', '0004_auto_20150831_1146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donation',
            options={'ordering': ['-created']},
        ),
        migrations.RemoveField(
            model_name='donation',
            name='donation_id',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='email',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='name',
        ),
        migrations.AddField(
            model_name='donation',
            name='charge_id',
            field=models.CharField(default='123ABC', help_text=b'The charge ID from Stripe.', max_length=100, verbose_name=b'Charge ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.DecimalField(max_digits=6, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='donation',
            name='message',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='donation',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
