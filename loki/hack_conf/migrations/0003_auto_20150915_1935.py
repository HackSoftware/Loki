# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0002_auto_20150915_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='co_speaker',
            field=models.ForeignKey(blank=True, related_name='co_schedule', null=True, to='hack_conf.Speaker'),
            preserve_default=True,
        ),
    ]
