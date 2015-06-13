# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('logo', models.URLField(blank=True)),
                ('jobs_link', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('comapny', models.OneToOneField(primary_key=True, serialize=False, to='base_app.Company')),
                ('description', ckeditor.fields.RichTextField()),
                ('facebook', models.URLField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('money_spent', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveSmallIntegerField(default=0)),
                ('twitter', models.URLField(null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
            ],
            options={
                'ordering': ('ordering',),
            },
            bases=(models.Model,),
        ),
    ]
