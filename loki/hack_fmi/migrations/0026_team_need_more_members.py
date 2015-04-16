# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0025_team_mentors'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='need_more_members',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
