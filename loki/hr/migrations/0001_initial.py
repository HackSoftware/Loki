# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0001_initial'),
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HR',
            fields=[
                ('baseuser_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, to=settings.AUTH_USER_MODEL, parent_link=True)),
                ('phone', models.CharField(max_length='20', null=True, blank=True)),
                ('company', models.ForeignKey(to='base_app.Partner')),
            ],
            options={
                'abstract': False,
            },
            bases=('hack_fmi.baseuser',),
        ),
    ]
