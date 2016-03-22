# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0021_auto_20160321_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='status',
            field=models.SmallIntegerField(default=6, choices=[(0, 'pending'), (1, 'running'), (2, 'ok'), (3, 'not_ok'), (4, 'submitted'), (5, 'missing'), (6, 'submitted_without_grading')]),
            preserve_default=True,
        ),
    ]
