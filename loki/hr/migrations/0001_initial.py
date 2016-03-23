# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HR',
            fields=[
                ('baseuser_ptr', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, auto_created=True, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(max_length='20', blank=True, null=True)),
                ('company', models.ForeignKey(to='base_app.Partner')),
            ],
            options={
                'abstract': False,
            },
            bases=('base_app.baseuser',),
        ),
    ]
