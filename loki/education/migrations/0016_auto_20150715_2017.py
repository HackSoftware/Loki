# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0015_oldcertificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oldcertificate',
            name='assignment',
            field=models.OneToOneField(to='education.CourseAssignment'),
            preserve_default=True,
        ),
    ]
