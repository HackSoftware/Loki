# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0003_remove_partner_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='logo',
        ),
    ]
