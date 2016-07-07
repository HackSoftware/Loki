# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0006_remove_team_mentors'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='mentors',
            field=models.ManyToManyField(through='hack_fmi.TeamMentorship', to='hack_fmi.Mentor'),
        ),
    ]
