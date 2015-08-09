# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_successviedeo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='successviedeo',
            old_name='picture',
            new_name='image',
        ),
    ]
