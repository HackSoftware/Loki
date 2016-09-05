# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-05 10:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationinfo',
            name='external_application_form',
            field=models.URLField(blank=True, help_text='Only add if course requires external application form', null=True),
        ),
    ]
