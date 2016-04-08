# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0006_auto_20160331_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=1000),
        ),
    ]
