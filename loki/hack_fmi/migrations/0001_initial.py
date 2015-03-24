# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=75)),
                ('avatar', models.ImageField(upload_to='')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('baseuser_ptr', models.OneToOneField(serialize=False, parent_link=True, primary_key=True, to='hack_fmi.BaseUser', auto_created=True)),
                ('faculty_number', models.SmallIntegerField()),
                ('shirt_size', models.SmallIntegerField(choices=[(1, 'S'), (2, 'M'), (3, 'L'), (4, 'XL')], default=1)),
            ],
            options={
                'abstract': False,
            },
            bases=('hack_fmi.baseuser',),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='competitor',
            name='known_technologies',
            field=models.ManyToManyField(to='hack_fmi.Language'),
            preserve_default=True,
        ),
    ]
