# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0018_auto_20150815_2043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solution',
            old_name='user',
            new_name='student',
        ),
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together=set([('student', 'task')]),
        ),
    ]
