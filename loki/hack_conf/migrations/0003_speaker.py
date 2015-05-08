# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0002_auto_20150505_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='Speaker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('facebook', models.URLField()),
                ('twitter', models.URLField()),
                ('google_plus', models.URLField()),
                ('github', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
