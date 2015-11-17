# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_auto_20150907_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='skype',
            field=models.CharField(max_length=20, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(max_length=20, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phone',
            field=models.CharField(max_length=20, blank=True, null=True),
            preserve_default=True,
        ),
    ]
