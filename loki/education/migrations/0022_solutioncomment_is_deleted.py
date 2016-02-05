# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0021_solutioncomment_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='solutioncomment',
            name='is_deleted',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
