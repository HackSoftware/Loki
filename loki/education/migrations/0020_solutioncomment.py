# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0019_auto_20160114_1834'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolutionComment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('writed_by', models.CharField(null=True, blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('write_rights', models.SmallIntegerField(choices=[(0, 'student'), (1, 'teacher')], default=0)),
                ('comment', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
