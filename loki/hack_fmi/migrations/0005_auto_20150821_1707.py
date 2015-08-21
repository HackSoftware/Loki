# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0006_company_logo'),
        ('hack_fmi', '0004_auto_20150623_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='birth_place',
            field=models.ForeignKey(to='base_app.City', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='baseuser',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
