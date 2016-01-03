# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0006_auto_20160103_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='build_id',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solution',
            name='url',
            field=models.URLField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
