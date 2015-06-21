# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkSubmission',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('verified_date', models.DateTimeField(null=True, blank=True)),
                ('tag', models.CharField(max_length=3, choices=[('COC', 'Code of Conduct'), ('DIV', 'Diversity Statement'), ('PRC', 'Problematic Conduct')])),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.CharField(null=True, max_length=256, blank=True)),
                ('project_has_tag', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('verified_date', models.DateTimeField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('homepage', models.CharField(null=True, max_length=256, blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('verified_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='project_verifications', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('message', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('resolved', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='reports', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RepresentationSubmission',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('verified_date', models.DateTimeField(null=True, blank=True)),
                ('public_message', models.TextField(null=True, blank=True)),
                ('private_message', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('project', models.ForeignKey(to='projects.Project', related_name='representation_submissions')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='representation_submissions')),
                ('verified_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='representationsubmission_verifications', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='linksubmission',
            name='project',
            field=models.ForeignKey(to='projects.Project', related_name='link_submissions'),
        ),
        migrations.AddField(
            model_name='linksubmission',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='link_submissions'),
        ),
        migrations.AddField(
            model_name='linksubmission',
            name='verified_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='linksubmission_verifications', blank=True),
        ),
    ]
