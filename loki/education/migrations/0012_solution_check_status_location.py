# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0011_auto_20160104_1944'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='check_status_location',
            field=models.CharField(default='', max_length=128),
            preserve_default=True,
        ),
    ]
