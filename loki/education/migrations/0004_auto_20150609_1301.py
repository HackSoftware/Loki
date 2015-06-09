# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0003_auto_20150609_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='github_account',
        ),
        migrations.RemoveField(
            model_name='student',
            name='linkedin_account',
        ),
    ]
