# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0011_auto_20150709_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='workingat',
            name='course_assignment',
            field=models.ForeignKey(blank=True, to='education.CourseAssignment', null=True),
            preserve_default=True,
        ),
    ]
