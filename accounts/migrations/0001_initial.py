# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=30)),
                ('email', models.EmailField(unique=True, max_length=80, verbose_name=b'email')),
                ('full_name', models.CharField(max_length=50, null=True, blank=True)),
                ('bio', models.TextField(max_length=140, null=True, blank=True)),
                ('website', models.CharField(max_length=90, null=True, blank=True)),
                ('edu_email', models.EmailField(max_length=80, unique=True, null=True, verbose_name=b'.edu email', blank=True)),
                ('gender', models.CharField(blank=True, max_length=6, null=True, choices=[(b'DUDE', b'Dude'), (b'BETTY', b'Betty')])),
                ('profile_picture', models.ImageField(null=True, upload_to=accounts.models.upload_location, blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_admin', models.BooleanField(default=False, verbose_name='admin')),
                ('is_verified', models.BooleanField(default=False, verbose_name='verified')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('followers', models.ManyToManyField(related_name='following', to='accounts.Follower')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
