# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0003_auto_20150820_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='title',
            field=models.SmallIntegerField(choices=[(1, 'Sponsor'), (2, 'General Media Partner'), (3, 'Branch Partner'), (5, 'School Partner')], default=1),
            preserve_default=True,
        ),
    ]
