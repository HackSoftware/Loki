# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_auto_20150612_2249'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='status',
        ),
    ]
