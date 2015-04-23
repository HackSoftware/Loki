# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0036_baseuser_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='from_company',
            field=models.ForeignKey(to='hack_fmi.Partner', null=True),
            preserve_default=True,
        ),
    ]
