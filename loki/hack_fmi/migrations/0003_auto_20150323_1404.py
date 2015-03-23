# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0002_auto_20150323_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='email',
            field=models.EmailField(max_length=75, unique=True),
            preserve_default=True,
        ),
    ]
