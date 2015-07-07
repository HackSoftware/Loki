# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='title',
            field=models.SmallIntegerField(default=1, choices=[(1, 'Sponsor'), (2, 'General Media Partner'), (3, 'Branch Partner'), (4, 'Media Partner')]),
            preserve_default=True,
        ),
    ]
