# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0028_team_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='room',
            field=models.ForeignKey(blank=True, to='hack_fmi.Room', null=True),
            preserve_default=True,
        ),
    ]
