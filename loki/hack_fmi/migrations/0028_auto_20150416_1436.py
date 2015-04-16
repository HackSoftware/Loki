# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0027_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='members_needed_desc',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='room',
            field=models.ForeignKey(null=True, blank=True, to='hack_fmi.Room'),
            preserve_default=True,
        ),
    ]
