# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20150831_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='bio',
            field=models.TextField(default='', max_length=140, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='edu_email',
            field=models.EmailField(unique=True, max_length=80, verbose_name=b'.edu email', null=True, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='full_name',
            field=models.CharField(default='', max_length=50, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='gender',
            field=models.CharField(default='', max_length=6, blank=True, choices=[(b'DUDE', b'Dude'), (b'BETTY', b'Betty')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='profile_picture',
            field=models.ImageField(default='', upload_to=accounts.models.upload_location, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='website',
            field=models.CharField(default='', max_length=90, blank=True),
            preserve_default=False,
        ),
    ]
