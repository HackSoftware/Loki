# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0017_auto_20160114_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='RetestSolution',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('status', models.SmallIntegerField(default=0, choices=[(0, 'pending'), (1, 'done')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('test_id', models.IntegerField()),
                ('tested_solutions_count', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='solution',
            name='status',
            field=models.SmallIntegerField(default=4, choices=[(0, 'pending'), (1, 'running'), (2, 'ok'), (3, 'not_ok'), (4, 'submitted')]),
            preserve_default=True,
        ),
    ]
