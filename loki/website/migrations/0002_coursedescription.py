# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_auto_20150907_2101'),
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.SlugField(unique=True, max_length=80)),
                ('short_description', models.CharField(max_length=300, blank=True)),
                ('description', ckeditor.fields.RichTextField()),
                ('video', models.URLField(blank=True)),
                ('SEO_description', models.CharField(max_length=255)),
                ('SEO_title', models.CharField(max_length=255)),
                ('course', models.OneToOneField(to='education.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
