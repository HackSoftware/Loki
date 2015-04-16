# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0028_team_members_needed_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='members_needed_desc',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
