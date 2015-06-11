# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0003_auto_20150608_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='lecture',
        ),
        migrations.AddField(
            model_name='lecture',
            name='course',
            field=models.ForeignKey(to='education.Course', blank=True, null=True),
            preserve_default=True,
        ),
    ]
