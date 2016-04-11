# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0005_auto_20160408_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='file',
            field=models.FileField(blank=True, upload_to='/solutions', null=True),
        ),
    ]
