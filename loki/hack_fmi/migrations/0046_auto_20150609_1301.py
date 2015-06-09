# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0045_auto_20150609_1247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='baseuser',
            old_name='github_account1',
            new_name='github_account',
        ),
        migrations.RenameField(
            model_name='baseuser',
            old_name='linkedin_account1',
            new_name='linkedin_account',
        ),
    ]
