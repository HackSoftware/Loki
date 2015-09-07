# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0004_auto_20150827_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sponsor',
            name='title',
            field=models.SmallIntegerField(choices=[(1, 'Sponsor'), (2, 'General Media Partner'), (3, 'Branch Partner'), (5, 'School Partner'), (6, 'Silver Sponsor'), (7, 'Gold Sponsor'), (8, 'Platinum Sponsor')], default=1),
            preserve_default=True,
        ),
    ]
