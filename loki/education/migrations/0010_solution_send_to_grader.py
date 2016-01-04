# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0009_graderrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='send_to_grader',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
