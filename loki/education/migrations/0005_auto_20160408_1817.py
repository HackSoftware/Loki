# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_auto_20160408_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='file',
            field=models.FileField(upload_to='/solutions', default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='binaryfiletest',
            name='file',
            field=models.FileField(upload_to='tests'),
        ),
    ]
