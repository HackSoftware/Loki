# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0019_auto_20150817_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='generate_certificates_until',
            field=models.DateField(default=datetime.datetime(2015, 8, 24, 13, 14, 57, 53003, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
