# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('mac', models.CharField(max_length=17)),
                ('date', models.DateField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('description', ckeditor.fields.RichTextField()),
                ('git_repository', models.CharField(max_length=256, blank=True)),
                ('image', models.ImageField(null=True, upload_to='courses_logoes', blank=True)),
                ('name', models.CharField(max_length=64)),
                ('short_description', models.CharField(max_length=300, blank=True)),
                ('show_on_index', models.BooleanField(default=False)),
                ('is_free', models.BooleanField(default=True)),
                ('application_until', models.DateField()),
                ('applications_url', models.URLField(null=True, blank=True)),
                ('ask_for_favorite_partner', models.BooleanField(default=False)),
                ('ask_for_feedback', models.BooleanField(default=False)),
                ('end_time', models.DateField(null=True, blank=True)),
                ('next_season_mail_list', models.URLField(null=True, blank=True)),
                ('SEO_description', models.CharField(max_length=255)),
                ('SEO_title', models.CharField(max_length=255)),
                ('start_time', models.DateField(null=True, blank=True)),
                ('url', models.SlugField(max_length=80, unique=True)),
                ('video', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseAssignment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('cv', models.FileField(null=True, upload_to='cvs', blank=True)),
                ('group_time', models.SmallIntegerField(choices=[(1, 'Early'), (2, 'Late')])),
                ('is_attending', models.BooleanField(default=True)),
                ('is_online', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
