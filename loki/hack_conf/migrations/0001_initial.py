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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('day', models.SmallIntegerField()),
                ('name', models.CharField(max_length=150)),
                ('time', models.TimeField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(blank=True, max_length=140)),
                ('description', models.TextField(blank=True)),
                ('picture', models.ImageField(upload_to='', blank=True)),
                ('facebook', models.URLField(blank=True)),
                ('twitter', models.URLField(blank=True)),
                ('google_plus', models.URLField(blank=True)),
                ('github', models.URLField(blank=True)),
                ('video_presentation', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.SmallIntegerField(choices=[(1, 'Sponsor'), (2, 'General Media Partner'), (3, 'Branch Partner'), (5, 'School Partner'), (6, 'Silver Sponsor'), (7, 'Gold Sponsor'), (8, 'Platinum Sponsor'), (9, 'General Partner')], default=1)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to='')),
            ],
        ),
        migrations.AddField(
            model_name='schedule',
            name='co_speaker',
            field=models.ForeignKey(null=True, to='hack_conf.Speaker', related_name='co_schedule', blank=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='speaker',
            field=models.ForeignKey(to='hack_conf.Speaker'),
        ),
    ]
