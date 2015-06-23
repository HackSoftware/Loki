# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0002_auto_20150618_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='full_image',
            field=models.ImageField(null=True, upload_to='', blank=True),
            preserve_default=True,
        ),
    ]
