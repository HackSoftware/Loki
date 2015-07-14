# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0012_workingat_course_assignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='workingat',
            name='came_working',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
