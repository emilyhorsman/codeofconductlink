# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20150621_1949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='tag',
            new_name='tags',
        ),
    ]
