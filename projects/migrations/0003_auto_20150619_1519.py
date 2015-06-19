# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0002_project_projectsubmission'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=3, choices=[('COC', 'Code of Conduct'), ('DIV', 'Diversity Statement'), ('PRC', 'Problematic Conduct')])),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('verified_date', models.DateTimeField(null=True, blank=True)),
                ('url', models.CharField(max_length=256, blank=True, null=True)),
                ('project_has_tag', models.BooleanField(default=False)),
                ('project', models.ForeignKey(to='projects.Project', related_name='link_submissions')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='link_submissions')),
                ('verified_by', models.ForeignKey(related_name='link_verifications', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RepresentationSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=256)),
                ('public_message', models.TextField(null=True, blank=True)),
                ('private_message', models.TextField(null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('verified_date', models.DateTimeField(null=True, blank=True)),
                ('project', models.ForeignKey(to='projects.Project', related_name='representation_submissions')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='representation_submissions')),
                ('verified_by', models.ForeignKey(related_name='representation_verifications', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='projectsubmission',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='project_submissions'),
        ),
        migrations.AlterField(
            model_name='projectsubmission',
            name='verified_by',
            field=models.ForeignKey(related_name='project_verifications', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
