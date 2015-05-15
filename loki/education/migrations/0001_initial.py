# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0004_partner'),
        ('hack_fmi', '0041_auto_20150515_1519'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('description', ckeditor.fields.RichTextField()),
                ('git_repository', models.CharField(blank=True, max_length=256)),
                ('image', models.ImageField(upload_to='courses_logoes', blank=True, null=True)),
                ('name', models.CharField(max_length=64)),
                ('short_description', models.CharField(blank=True, max_length=300)),
                ('show_on_index', models.BooleanField(default=False)),
                ('is_free', models.BooleanField(default=True)),
                ('application_until', models.DateField()),
                ('applications_url', models.URLField(blank=True, null=True)),
                ('ask_for_favorite_partner', models.BooleanField(default=False)),
                ('ask_for_feedback', models.BooleanField(default=False)),
                ('end_time', models.DateField(blank=True, null=True)),
                ('next_season_mail_list', models.URLField(blank=True, null=True)),
                ('SEO_description', models.CharField(max_length=255)),
                ('SEO_title', models.CharField(max_length=255)),
                ('start_time', models.DateField(blank=True, null=True)),
                ('url', models.SlugField(max_length=80, unique=True)),
                ('video', models.URLField(blank=True)),
                ('partner', models.ManyToManyField(blank=True, null=True, to='base_app.Partner')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseAssignment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('cv', models.FileField(upload_to='cvs', blank=True, null=True)),
                ('group_time', models.SmallIntegerField(choices=[(1, 'Early'), (2, 'Late')])),
                ('is_attending', models.BooleanField(default=True)),
                ('points', models.PositiveIntegerField(default=0)),
                ('is_online', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='education.Course')),
                ('favourite_partners', models.ManyToManyField(blank=True, null=True, to='base_app.Partner')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('baseuser_ptr', models.OneToOneField(auto_created=True, to=settings.AUTH_USER_MODEL, serialize=False, parent_link=True, primary_key=True)),
                ('status', models.SmallIntegerField(default=1, choices=[(1, 'Student'), (2, 'HR'), (3, 'Teacher')])),
                ('description', models.TextField(blank=True)),
                ('github_account', models.URLField(blank=True, null=True)),
                ('linkedin_account', models.URLField(blank=True, null=True)),
                ('mac', models.CharField(blank=True, null=True, max_length=17)),
                ('studies_at', models.CharField(blank=True, null=True, max_length='110')),
                ('works_at', models.CharField(blank=True, null=True, max_length='110')),
                ('phone', models.CharField(blank=True, null=True, max_length='20')),
                ('courses', models.ManyToManyField(through='education.CourseAssignment', to='education.Course')),
                ('hr_of', models.ForeignKey(blank=True, null=True, to='base_app.Partner')),
            ],
            options={
                'abstract': False,
            },
            bases=('hack_fmi.baseuser',),
        ),
        migrations.AddField(
            model_name='courseassignment',
            name='user',
            field=models.ForeignKey(to='education.Student'),
            preserve_default=True,
        ),
    ]
