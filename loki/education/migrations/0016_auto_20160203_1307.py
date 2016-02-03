# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import education.validators


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0015_auto_20160106_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='url',
            field=models.URLField(null=True, blank=True, validators=[education.validators.validate_github_url]),
            preserve_default=True,
        ),
    ]
