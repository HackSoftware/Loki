# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0002_auto_20160330_1315'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='faculty',
            options={'verbose_name_plural': 'Faculties'},
        ),
        migrations.AlterModelOptions(
            name='university',
            options={'verbose_name_plural': 'Universities'},
        ),
        migrations.AlterField(
            model_name='educationplace',
            name='name',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterUniqueTogether(
            name='educationplace',
            unique_together=set([('name', 'city')]),
        ),
    ]
