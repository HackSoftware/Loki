# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0013_auto_20160105_1742'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='send_to_grader',
            new_name='gradable',
        ),
    ]
