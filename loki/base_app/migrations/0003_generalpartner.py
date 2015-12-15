# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0002_auto_20150907_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralPartner',
            fields=[
                ('partner', models.OneToOneField(primary_key=True, serialize=False, to='base_app.Partner')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
