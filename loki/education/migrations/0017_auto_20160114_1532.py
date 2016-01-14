# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0016_auto_20160113_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='status',
            field=models.SmallIntegerField(default=0, choices=[(0, 'pending'), (1, 'running'), (2, 'ok'), (3, 'not_ok'), (4, 'submitted')]),
            preserve_default=True,
        ),
    ]
