# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-24 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0032_auto_20161115_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='looking_for_job',
            field=models.BooleanField(default=False),
        ),
    ]