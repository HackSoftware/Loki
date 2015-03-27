# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0005_auto_20150325_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='is_vegetarian',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
