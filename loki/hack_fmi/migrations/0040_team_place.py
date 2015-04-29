# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0039_team_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='place',
            field=models.SmallIntegerField(null=True),
            preserve_default=True,
        ),
    ]
