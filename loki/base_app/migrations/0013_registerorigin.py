# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0012_auto_20160406_1155'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterOrigin',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.SlugField()),
                ('redirect_url', models.URLField()),
            ],
        ),
    ]
