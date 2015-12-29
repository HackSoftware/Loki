# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_auto_20151229_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='code',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='solution',
            name='code',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='test',
            name='code',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
