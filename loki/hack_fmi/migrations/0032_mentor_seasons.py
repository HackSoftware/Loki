# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0031_auto_20150417_1024'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='seasons',
            field=models.ManyToManyField(to='hack_fmi.Season'),
            preserve_default=True,
        ),
    ]
