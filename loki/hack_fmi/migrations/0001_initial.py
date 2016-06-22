# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(null=True, max_length=100)),
                ('topic', models.CharField(max_length=100)),
                ('front_page', ckeditor.fields.RichTextField(blank=True)),
                ('min_team_members_count', models.SmallIntegerField(default=1)),
                ('max_team_members_count', models.SmallIntegerField(default=6)),
                ('sign_up_deadline', models.DateField()),
                ('make_team_dead_line', models.DateField()),
                ('mentor_pick_start_date', models.DateField()),
                ('mentor_pick_end_date', models.DateField()),
                ('max_mentor_pick', models.SmallIntegerField(default=1)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
