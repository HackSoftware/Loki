# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='studies_at',
            field=models.CharField(null=True, max_length=110, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='works_at',
            field=models.CharField(null=True, max_length=110, blank=True),
            preserve_default=True,
        ),
    ]
