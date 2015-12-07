# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0002_auto_20150907_2101'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partner',
            old_name='comapny',
            new_name='company',
        ),
    ]
