# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-14 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0035_course_deadline_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='english_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
