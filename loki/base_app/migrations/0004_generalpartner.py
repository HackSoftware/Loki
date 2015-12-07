# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0003_auto_20151207_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralPartner',
            fields=[
                ('partner', models.OneToOneField(serialize=False, primary_key=True, to='base_app.Partner')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
