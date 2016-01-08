# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_auto_20160103_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='task',
            field=models.OneToOneField(to='education.Task'),
            preserve_default=True,
        ),
    ]
