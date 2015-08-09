# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0004_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='logo',
            new_name='logo_url',
        ),
    ]
