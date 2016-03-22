# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0018_auto_20160114_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retestsolution',
            name='tested_solutions_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
