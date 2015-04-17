# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0030_season_front_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='mentors',
            field=models.ManyToManyField(blank=True, to='hack_fmi.Mentor', null=True),
            preserve_default=True,
        ),
    ]
