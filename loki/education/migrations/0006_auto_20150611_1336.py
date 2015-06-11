# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0005_auto_20150611_1324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='studies_at',
        ),
        migrations.RemoveField(
            model_name='student',
            name='works_at',
        ),
    ]
