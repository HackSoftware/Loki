# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0003_speaker'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='description',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='speaker',
            name='picture',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
