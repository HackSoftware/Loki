# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0016_auto_20150715_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oldcertificate',
            name='url_id',
            field=models.PositiveIntegerField(unique=True),
            preserve_default=True,
        ),
    ]
