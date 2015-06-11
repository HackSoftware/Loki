# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0048_auto_20150611_1324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='baseuser',
            old_name='studies_at1',
            new_name='studies_at',
        ),
        migrations.RenameField(
            model_name='baseuser',
            old_name='works_at1',
            new_name='works_at',
        ),
    ]
