# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0015_auto_20150330_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='needs_work',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='season',
            field=models.ForeignKey(to='hack_fmi.Season', default=0),
            preserve_default=True,
        ),
    ]
