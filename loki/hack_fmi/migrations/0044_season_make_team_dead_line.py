# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0043_auto_20150519_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='make_team_dead_line',
            field=models.DateField(default=datetime.datetime(2015, 5, 20, 8, 17, 9, 426363, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
