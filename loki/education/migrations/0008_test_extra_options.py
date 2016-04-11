# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0007_auto_20160411_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='extra_options',
            field=models.TextField(null=True, blank=True),
        ),
    ]
