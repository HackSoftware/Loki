# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-06 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_coursedescription_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursedescription',
            name='logo',
        ),
    ]