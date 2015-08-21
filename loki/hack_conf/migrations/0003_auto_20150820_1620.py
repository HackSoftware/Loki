# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0002_sponsor_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='title',
            field=models.CharField(blank=True, max_length=140),
            preserve_default=True,
        ),
    ]
