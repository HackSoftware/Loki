# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_auto_20150615_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='hr_of',
        ),
    ]
