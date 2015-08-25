# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import photos.models


class Migration(migrations.Migration):

    dependencies = [
        ('hashtags', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('border_color', models.CharField(default=b'#', max_length=7)),
                ('featured', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.TextField(max_length=250, blank=True)),
                ('hashtag_enabled_description', models.TextField(help_text=b'Contains the description with hashtags replaced with links', blank=True)),
                ('featured', models.BooleanField(default=False)),
                ('photo', models.ImageField(upload_to=photos.models.upload_location)),
                ('slug', models.SlugField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(to='photos.Category')),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('hashtags', models.ManyToManyField(to='hashtags.Hashtag', blank=True)),
                ('likers', models.ManyToManyField(related_name='likers', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='photo',
            unique_together=set([('slug', 'category')]),
        ),
    ]
