# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0002_auto_20150613_1457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='name',
        ),
    ]
