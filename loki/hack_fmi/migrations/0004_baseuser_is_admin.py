# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0003_auto_20150323_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='is_admin',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
