# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0010_auto_20150327_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
