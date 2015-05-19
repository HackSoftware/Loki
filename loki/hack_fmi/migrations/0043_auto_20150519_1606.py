# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0042_auto_20150519_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='season',
            name='number',
        ),
        migrations.AddField(
            model_name='season',
            name='name',
            field=models.CharField(null=True, max_length=100),
            preserve_default=True,
        ),
    ]
