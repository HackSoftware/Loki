# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0018_competitor_social_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='season',
            field=models.ForeignKey(default=1, to='hack_fmi.Season'),
            preserve_default=True,
        ),
    ]
