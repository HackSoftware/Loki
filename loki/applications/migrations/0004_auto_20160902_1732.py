# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-02 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0003_auto_20160901_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='skype',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='studies_at',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='works_at',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
