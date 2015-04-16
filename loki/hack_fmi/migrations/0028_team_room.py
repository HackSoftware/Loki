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
            name='room',
            field=models.ForeignKey(blank=True, default=0, to='hack_fmi.Room'),
            preserve_default=False,
        ),
    ]
