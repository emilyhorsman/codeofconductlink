# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectSubmission',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('verified_date', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('homepage', models.CharField(blank=True, max_length=256, null=True)),
                ('tags', models.CharField(blank=True, max_length=256, null=True)),
                ('project', models.ForeignKey(to='projects.Project', related_name='submissions')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='submitted_by')),
                ('verified_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True, related_name='verified_by')),
            ],
        ),
    ]
