# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0041_auto_20150515_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitor',
            name='faculty_number',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
