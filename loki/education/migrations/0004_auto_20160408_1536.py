# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_auto_20160408_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='task',
            field=models.ForeignKey(to='education.Task'),
        ),
    ]
