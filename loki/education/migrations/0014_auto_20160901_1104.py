# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-01 08:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0013_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='ask_for_favorite_partner',
        ),
        migrations.RemoveField(
            model_name='course',
            name='ask_for_feedback',
        ),
        migrations.RemoveField(
            model_name='course',
            name='next_season_mail_list',
        ),
    ]
