# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0003_baseuser_full_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='avatar',
            field=models.ImageField(null=True, upload_to='', blank=True),
            preserve_default=True,
        ),
    ]
