# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0034_auto_20150422_1452'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseuser',
            name='is_admin',
        ),
    ]
