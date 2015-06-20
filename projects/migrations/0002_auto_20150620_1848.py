# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linksubmission',
            name='verified_by',
            field=models.ForeignKey(blank=True, null=True, related_name='linksubmission_verifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='representationsubmission',
            name='verified_by',
            field=models.ForeignKey(blank=True, null=True, related_name='representationsubmission_verifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
