# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-02 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0026_material'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='presentation_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
