# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0037_auto_20150423_0927'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mentor',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='mentor',
            name='order',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
