# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_auto_20150517_1618'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseassignment',
            name='points',
        ),
        migrations.RemoveField(
            model_name='student',
            name='description',
        ),
    ]
