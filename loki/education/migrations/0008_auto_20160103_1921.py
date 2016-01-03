# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0007_auto_20160103_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'pending'), (1, 'running'), (2, 'ok'), (3, 'not_ok')], default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='test_type',
            field=models.SmallIntegerField(choices=[(0, 'unittest')], default=0),
            preserve_default=True,
        ),
    ]
