# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0006_auto_20150622_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='fb_group',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
