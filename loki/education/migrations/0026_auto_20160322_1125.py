# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0025_auto_20160322_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='token',
            field=models.CharField(max_length=110, unique=True, default=uuid.uuid4),
        ),
    ]
