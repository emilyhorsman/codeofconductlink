# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('verified_date', models.DateTimeField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('homepage', models.URLField(null=True, blank=True)),
                ('code_of_conduct', models.URLField(null=True, blank=True)),
                ('tags', taggit.managers.TaggableManager(through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('verified_by', models.ForeignKey(related_name='project_verifications', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('message', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('resolved', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='reports', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('verified_date', models.DateTimeField(null=True, blank=True)),
                ('is_contributor', models.BooleanField(default=False)),
                ('url', models.URLField()),
                ('public_message', models.TextField(null=True, blank=True)),
                ('private_message', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('project', models.ForeignKey(related_name='submissions', to='projects.Project')),
                ('tag', taggit.managers.TaggableManager(through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags', to='taggit.Tag')),
                ('user', models.ForeignKey(related_name='submissions', to=settings.AUTH_USER_MODEL)),
                ('verified_by', models.ForeignKey(related_name='submission_verifications', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vouch',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(related_name='vouches', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
