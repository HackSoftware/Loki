# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0012_auto_20150328_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='activation_code',
            field=models.CharField(max_length=32, default='123'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='is_active',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
