# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0008_courseassignment_student_presence'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='courseassignment',
            unique_together=set([('user', 'course')]),
        ),
    ]
