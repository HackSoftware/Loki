# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0003_auto_20151117_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('build_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code', models.TextField(blank=True, null=True)),
                ('status', models.SmallIntegerField(default=1, choices=[(1, 'pending'), (2, 'running'), (3, 'done'), (4, 'failed')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProgrammingLanguage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=110)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('code', models.TextField(blank=True, null=True)),
                ('github_url', models.URLField()),
                ('test_type', models.SmallIntegerField(default=1, choices=[(1, 'unittest')])),
                ('language', models.ForeignKey(to='education.ProgrammingLanguage')),
                ('task', models.ForeignKey(to='education.Task')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='build',
            name='test',
            field=models.ForeignKey(to='education.Test'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='solution',
            name='code',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
