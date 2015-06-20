# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkSubmission',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('verified_date', models.DateTimeField(null=True, blank=True)),
                ('tag', models.CharField(choices=[('COC', 'Code of Conduct'), ('DIV', 'Diversity Statement'), ('PRC', 'Problematic Conduct')], max_length=3)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('url', models.CharField(null=True, blank=True, max_length=256)),
                ('project_has_tag', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('verified_date', models.DateTimeField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(unique=True, max_length=256)),
                ('homepage', models.CharField(null=True, blank=True, max_length=256)),
                ('tags', models.CharField(null=True, blank=True, max_length=256)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('verified_by', models.ForeignKey(related_name='project_verifications', to=settings.AUTH_USER_MODEL, null=True, blank=True)),
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
                ('user', models.ForeignKey(related_name='reports', to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RepresentationSubmission',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('verified_date', models.DateTimeField(null=True, blank=True)),
                ('tag', models.CharField(max_length=256)),
                ('public_message', models.TextField(null=True, blank=True)),
                ('private_message', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('project', models.ForeignKey(related_name='representation_submissions', to='projects.Project')),
                ('user', models.ForeignKey(related_name='representation_submissions', to=settings.AUTH_USER_MODEL)),
                ('verified_by', models.ForeignKey(related_name='representation_verifications', to=settings.AUTH_USER_MODEL, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='linksubmission',
            name='project',
            field=models.ForeignKey(related_name='link_submissions', to='projects.Project'),
        ),
        migrations.AddField(
            model_name='linksubmission',
            name='user',
            field=models.ForeignKey(related_name='link_submissions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='linksubmission',
            name='verified_by',
            field=models.ForeignKey(related_name='link_verifications', to=settings.AUTH_USER_MODEL, null=True, blank=True),
        ),
    ]
