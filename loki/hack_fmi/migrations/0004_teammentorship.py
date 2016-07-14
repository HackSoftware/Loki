# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0003_auto_20160622_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMentorship',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('mentor', models.ForeignKey(to='hack_fmi.Mentor')),
                ('team', models.ForeignKey(to='hack_fmi.Team')),
            ],
        ),
    ]
