# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20151009_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursedescription',
            name='blog_article',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
    ]
