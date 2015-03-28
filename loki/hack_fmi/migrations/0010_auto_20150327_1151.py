# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0009_auto_20150327_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='repository',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
