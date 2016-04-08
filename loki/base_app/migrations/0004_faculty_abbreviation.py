# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0003_auto_20160331_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='abbreviation',
            field=models.CharField(max_length=10, blank=True, null=True),
        ),
    ]
