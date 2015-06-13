# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0001_initial'),
        ('base_app', '0001_initial'),
        ('education', '0002_auto_20150612_2249'),
    ]

    operations = [
        migrations.CreateModel(
            name='HR',
            fields=[
                ('baseuser_ptr', models.OneToOneField(parent_link=True, auto_created=True, serialize=False, primary_key=True, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(max_length='20', null=True, blank=True)),
                ('company', models.ForeignKey(to='base_app.Partner')),
                ('teached_courses', models.ManyToManyField(to='education.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=('hack_fmi.baseuser',),
        ),
    ]
