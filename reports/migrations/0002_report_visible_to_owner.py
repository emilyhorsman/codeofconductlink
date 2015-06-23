# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='visible_to_owner',
            field=models.BooleanField(help_text='I want to let the owner of this content see this report. If I do not opt-in explicitly, the owner will not see my report.', default=False),
        ),
    ]
