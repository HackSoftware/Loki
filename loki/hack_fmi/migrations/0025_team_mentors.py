# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0024_season_max_mentor_pick'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='mentors',
            field=models.ManyToManyField(to='hack_fmi.Mentor'),
            preserve_default=True,
        ),
    ]
