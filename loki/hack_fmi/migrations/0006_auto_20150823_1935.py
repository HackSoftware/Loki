# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0005_auto_20150821_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='birth_place',
            field=models.ForeignKey(blank=True, null=True, to='base_app.City'),
            preserve_default=True,
        ),
    ]
