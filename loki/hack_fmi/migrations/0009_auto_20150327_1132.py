# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0008_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('is_leader', models.BooleanField(default=False)),
                ('competitor', models.ForeignKey(to='hack_fmi.Competitor')),
                ('team', models.ForeignKey(to='hack_fmi.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='team',
            name='teammates',
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(through='hack_fmi.TeamMembership', to='hack_fmi.Competitor'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=100, unique=True),
            preserve_default=True,
        ),
    ]
