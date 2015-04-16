# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0026_team_need_more_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('capacity', models.SmallIntegerField()),
                ('season', models.ForeignKey(to='hack_fmi.Season')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
