# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from hack_fmi.models import TeamMentorship, Team


def move_m2m_data_to_team_mentorship_model(apps, schema_editor):
    teams = Team.objects.all()
    for team in teams:
        for mentor in team.mentors.all():
            TeamMentorship.objects.create(
                team=team,
                mentor=mentor
            )


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0004_teammentorship'),
    ]

    operations = [
        migrations.RunPython(move_m2m_data_to_team_mentorship_model),
    ]
