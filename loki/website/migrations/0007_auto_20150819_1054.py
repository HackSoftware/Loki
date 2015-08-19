# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20150818_1853'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Successor',
            new_name='SuccessStoryPerson',
        ),
    ]
