# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0023_teacher_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='token',
            field=models.CharField(max_length=110, null=True, default=uuid.uuid4),
        ),
    ]
