# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0004_baseuser_is_admin'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Language',
            new_name='Skill',
        ),
        migrations.RenameField(
            model_name='competitor',
            old_name='known_technologies',
            new_name='known_skills',
        ),
    ]
