# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0004_city'),
        ('education', '0009_auto_20150702_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WorkingAt',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100, null=True, blank=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('company', models.ForeignKey(to='education.Company', blank=True, null=True)),
                ('location', models.ForeignKey(to='base_app.City')),
                ('student', models.ForeignKey(to='education.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
