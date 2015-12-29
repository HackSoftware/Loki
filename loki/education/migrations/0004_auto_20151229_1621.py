# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0003_auto_20151117_1227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('build_id', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('build_status', model_utils.fields.StatusField(max_length=100, choices=[('pending', 'pending'), ('running', 'running'), ('done', 'done'), ('failed', 'failed')], no_check_for_status=True, default='pending', db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuildResult',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('return_code', models.TextField()),
                ('output', models.TextField()),
                ('result_status', model_utils.fields.StatusField(choices=[('ok', 'ok'), ('not_ok', 'not_ok')], no_check_for_status=True, default='ok', max_length=100)),
                ('build', models.ForeignKey(to='education.Build')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProgrammingLanguage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=110)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('code', models.TextField()),
                ('github_url', models.URLField()),
                ('test_type', model_utils.fields.StatusField(max_length=100, choices=[('unittest', 'unittest')], no_check_for_status=True, default='unittest', db_index=True)),
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
    ]
