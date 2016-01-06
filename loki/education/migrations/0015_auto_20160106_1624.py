# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0014_auto_20160105_1745'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='return_code',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='solution',
            name='test_output',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
