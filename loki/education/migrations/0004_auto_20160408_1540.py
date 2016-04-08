# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0003_auto_20160408_1537'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='code',
        ),
        migrations.RemoveField(
            model_name='test',
            name='description',
        ),
        migrations.RenameField(
            model_name='sourcecodetest',
            old_name='sourcecode',
            new_name='code',
        ),
        migrations.AlterField(
            model_name='test',
            name='task',
            field=models.OneToOneField(to='education.Task'),
        ),
    ]
