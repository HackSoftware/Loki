# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0022_auto_20150407_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='max_team_members_count',
            field=models.SmallIntegerField(default=6),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='season',
            name='mentor_pick_end_date',
            field=models.DateField(default=datetime.datetime(2015, 4, 14, 8, 14, 50, 831108, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='season',
            name='mentor_pick_start_date',
            field=models.DateField(default=datetime.datetime(2015, 4, 14, 8, 15, 5, 82960, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='season',
            name='min_team_members_count',
            field=models.SmallIntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='season',
            name='sign_up_deadline',
            field=models.DateField(default=datetime.datetime(2015, 4, 14, 8, 15, 35, 66797, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='season',
            name='topic',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
    ]
