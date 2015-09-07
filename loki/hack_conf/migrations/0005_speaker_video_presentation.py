# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0004_auto_20150827_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='video_presentation',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
