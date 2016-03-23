# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDescription',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('logo', models.CharField(help_text='Copy class from <a href="http://devicon.fr/" target="_blank">www.devicon.fr</a>', max_length=255, blank=True)),
                ('custom_logo', models.ImageField(help_text='Add a custom course logo with 308x308 size.', blank=True, upload_to='')),
                ('url', models.SlugField(max_length=80, unique=True)),
                ('video_image', models.ImageField(help_text='Add a 16/9 video cover image.', blank=True, upload_to='')),
                ('blog_article', models.CharField(max_length=255, blank=True)),
                ('course_intensity', models.PositiveIntegerField(default=0)),
                ('course_days', models.CharField(max_length=255, blank=True)),
                ('paid_course', models.BooleanField(default=False)),
                ('course_summary', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('teacher_preview', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('realization', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('price', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('address', models.CharField(help_text='Add <a href="http://www.google.com/maps" target="_blank">google maps</a> link to HackBulgaria location', max_length=255, blank=True)),
                ('SEO_description', models.CharField(max_length=255)),
                ('SEO_title', models.CharField(max_length=255)),
                ('course', models.OneToOneField(to='education.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('label', models.CharField(max_length=80, unique=True)),
                ('text', ckeditor.fields.RichTextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SuccessStoryPerson',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('title', models.CharField(max_length=100, blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='SuccessVideo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('youtube_link', models.URLField(blank=True)),
            ],
        ),
    ]
