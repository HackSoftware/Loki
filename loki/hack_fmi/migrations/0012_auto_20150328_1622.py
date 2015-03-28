# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0011_baseuser_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='description',
            new_name='idea_description',
        ),
    ]
