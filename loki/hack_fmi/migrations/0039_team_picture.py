# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0038_auto_20150424_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='picture',
            field=models.ImageField(upload_to='', blank=True),
            preserve_default=True,
        ),
    ]
