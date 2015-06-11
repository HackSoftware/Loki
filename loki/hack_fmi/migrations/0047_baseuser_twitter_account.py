# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0046_auto_20150609_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='twitter_account',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
