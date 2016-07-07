# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0005_auto_20160707_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='mentors',
        ),
    ]
