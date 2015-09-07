# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac', models.CharField(max_length=17)),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', ckeditor.fields.RichTextField()),
                ('git_repository', models.CharField(blank=True, max_length=256)),
                ('image', models.ImageField(null=True, blank=True, upload_to='courses_logoes')),
                ('name', models.CharField(max_length=64)),
                ('short_description', models.CharField(blank=True, max_length=300)),
                ('show_on_index', models.BooleanField(default=False)),
                ('is_free', models.BooleanField(default=True)),
                ('application_until', models.DateField()),
                ('applications_url', models.URLField(null=True, blank=True)),
                ('ask_for_favorite_partner', models.BooleanField(default=False)),
                ('ask_for_feedback', models.BooleanField(default=False)),
                ('end_time', models.DateField(null=True, blank=True)),
                ('fb_group', models.URLField(null=True, blank=True)),
                ('next_season_mail_list', models.URLField(null=True, blank=True)),
                ('SEO_description', models.CharField(max_length=255)),
                ('SEO_title', models.CharField(max_length=255)),
                ('start_time', models.DateField(null=True, blank=True)),
                ('url', models.SlugField(max_length=80, unique=True)),
                ('video', models.URLField(blank=True)),
                ('generate_certificates_until', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.FileField(null=True, blank=True, upload_to='cvs')),
                ('group_time', models.SmallIntegerField(choices=[(1, 'Early'), (2, 'Late')])),
                ('is_attending', models.BooleanField(default=True)),
                ('student_presence', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('is_online', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
