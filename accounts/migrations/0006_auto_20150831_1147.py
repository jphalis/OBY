# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150831_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='edu_email',
            field=models.EmailField(max_length=80, unique=True, null=True, verbose_name=b'.edu email', blank=True),
        ),
    ]
