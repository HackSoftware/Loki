# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-19 13:43
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0012_auto_20160810_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseApplyTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', ckeditor.fields.RichTextField()),
                ('url', models.URLField(blank=True, null=True)),
                ('apply_for_courses', models.ManyToManyField(to='education.Course')),
            ],
        ),
    ]