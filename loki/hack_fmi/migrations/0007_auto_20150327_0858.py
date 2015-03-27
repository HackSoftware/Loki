# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0006_competitor_is_vegetarian'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitor',
            name='faculty_number',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
