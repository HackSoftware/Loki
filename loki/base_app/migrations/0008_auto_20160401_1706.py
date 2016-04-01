# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0007_auto_20160331_1635'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='academy',
            options={'verbose_name_plural': 'Academies'},
        ),
        migrations.RenameField(
            model_name='faculty',
            old_name='uni',
            new_name='university',
        ),
        migrations.AlterUniqueTogether(
            name='faculty',
            unique_together=set([('university', 'name')]),
        ),
    ]
