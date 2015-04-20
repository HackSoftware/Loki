# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0031_auto_20150417_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='mentors',
            field=models.ManyToManyField(to='hack_fmi.Mentor', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='technologies',
            field=models.ManyToManyField(to='hack_fmi.Skill', blank=True),
            preserve_default=True,
        ),
    ]
