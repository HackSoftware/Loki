# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0012_auto_20160406_1155'),
    ]

    operations = [
        migrations.CreateModel(
            name='HostingPartner',
            fields=[
                ('partner', models.OneToOneField(to='base_app.Partner', serialize=False, primary_key=True)),
            ],
        ),
    ]
