# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0012_solution_check_status_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='check_status_location',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
    ]
