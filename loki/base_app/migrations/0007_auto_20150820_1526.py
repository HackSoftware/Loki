# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0006_company_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 20, 12, 26, 13, 928500, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=255, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2015, 8, 20, 12, 26, 34, 192614, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
