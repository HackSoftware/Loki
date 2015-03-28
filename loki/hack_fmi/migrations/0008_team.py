# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0007_auto_20150327_0858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('repository', models.URLField()),
                ('teammates', models.ForeignKey(to='hack_fmi.Competitor')),
                ('technologies', models.ManyToManyField(to='hack_fmi.Skill')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
