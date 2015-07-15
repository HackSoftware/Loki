# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0013_workingat_came_working'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workingat',
            name='course_assignment',
        ),
        migrations.AddField(
            model_name='workingat',
            name='course',
            field=models.ForeignKey(null=True, blank=True, to='education.Course'),
            preserve_default=True,
        ),
    ]
