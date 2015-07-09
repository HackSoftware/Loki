# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0010_company_workingat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workingat',
            name='company',
            field=models.ForeignKey(blank=True, null=True, to='base_app.Company'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Company',
        ),
    ]
