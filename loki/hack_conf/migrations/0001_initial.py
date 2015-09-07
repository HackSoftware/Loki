# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.SmallIntegerField()),
                ('name', models.CharField(max_length=150)),
                ('time', models.TimeField()),
                ('description', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(blank=True, max_length=140)),
                ('description', models.TextField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('facebook', models.URLField(blank=True)),
                ('twitter', models.URLField(blank=True)),
                ('google_plus', models.URLField(blank=True)),
                ('github', models.URLField(blank=True)),
                ('video_presentation', models.URLField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.SmallIntegerField(choices=[(1, 'Sponsor'), (2, 'General Media Partner'), (3, 'Branch Partner'), (5, 'School Partner'), (6, 'Silver Sponsor'), (7, 'Gold Sponsor'), (8, 'Platinum Sponsor')], default=1)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='schedule',
            name='author',
            field=models.ForeignKey(to='hack_conf.Speaker'),
            preserve_default=True,
        ),
    ]
