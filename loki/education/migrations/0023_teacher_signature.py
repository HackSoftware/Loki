# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0022_auto_20160321_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='signature',
            field=models.ImageField(upload_to='teachers_signatures', blank=True, null=True),
            preserve_default=True,
        ),
    ]
