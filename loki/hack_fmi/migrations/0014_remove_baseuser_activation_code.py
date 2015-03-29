# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0013_auto_20150329_0914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='baseuser',
            name='activation_code',
        ),
    ]
