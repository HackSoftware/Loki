# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0023_auto_20150414_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='max_mentor_pick',
            field=models.SmallIntegerField(default=1),
            preserve_default=True,
        ),
    ]
