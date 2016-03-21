# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0020_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'pending'), (1, 'running'), (2, 'ok'), (3, 'not_ok'), (4, 'submitted'), (5, 'missing'), (6, 'submitted_without_grading')], default=4),
            preserve_default=True,
        ),
    ]
