# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0006_company_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='video_presentation',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
