# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0035_remove_baseuser_is_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='is_staff',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
