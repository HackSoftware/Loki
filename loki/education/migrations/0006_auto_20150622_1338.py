# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0005_remove_student_hr_of'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentnote',
            name='post_time',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
