# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('logo_url', models.URLField(blank=True)),
                ('logo', models.ImageField(null=True, blank=True, upload_to='partners_logoes')),
                ('jobs_link', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('url', models.URLField(null=True, blank=True)),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('comapny', models.OneToOneField(serialize=False, to='base_app.Company', primary_key=True)),
                ('description', ckeditor.fields.RichTextField()),
                ('facebook', models.URLField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('money_spent', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveSmallIntegerField(default=0)),
                ('twitter', models.URLField(null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('video_presentation', models.URLField(null=True, blank=True)),
            ],
            options={
                'ordering': ('ordering',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
