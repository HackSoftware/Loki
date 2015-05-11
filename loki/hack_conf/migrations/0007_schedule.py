# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0006_sponsor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('time', models.CharField(max_length=10)),
                ('description', models.TextField(blank=True)),
                ('author', models.ForeignKey(to='hack_conf.Speaker')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
