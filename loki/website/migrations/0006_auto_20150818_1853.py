# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_snippet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='label',
            field=models.CharField(unique=True, max_length=80),
            preserve_default=True,
        ),
    ]
