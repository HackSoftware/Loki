# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-22 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0009_remove_team_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='other_skills',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]
