# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0005_auto_20160103_1636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='build',
            name='test',
        ),
        migrations.DeleteModel(
            name='Build',
        ),
        migrations.AddField(
            model_name='solution',
            name='build_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solution',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 3, 15, 16, 47, 975208, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='solution',
            name='status',
            field=models.SmallIntegerField(choices=[(1, 'pending'), (2, 'running'), (3, 'done'), (4, 'failed')], default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='solution',
            name='code',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together=set([]),
        ),
    ]
