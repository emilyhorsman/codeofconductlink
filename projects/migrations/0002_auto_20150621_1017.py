# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=taggit.managers.TaggableManager(verbose_name='Tags', blank=True, to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.'),
        ),
        migrations.AlterField(
            model_name='representationsubmission',
            name='tags',
            field=taggit.managers.TaggableManager(verbose_name='Tags', blank=True, to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.'),
        ),
    ]
