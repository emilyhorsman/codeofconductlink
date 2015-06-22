# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='report',
            name='user',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]
