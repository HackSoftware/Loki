# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.management import call_command


def load_fixtures(apps, schema_editor):
    call_command('loaddata', 'load_season', app_label='hack_fmi')


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixtures)
    ]
