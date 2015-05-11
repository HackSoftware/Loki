# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0007_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='day',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
