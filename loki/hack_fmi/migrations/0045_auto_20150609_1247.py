# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0044_season_make_team_dead_line'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='github_account1',
            field=models.URLField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='baseuser',
            name='linkedin_account1',
            field=models.URLField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
