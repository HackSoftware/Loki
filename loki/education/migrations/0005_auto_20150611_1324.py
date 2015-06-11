# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import education.validators


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_auto_20150609_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='mac',
            field=models.CharField(validators=[education.validators.validate_mac], max_length=17, null=True, blank=True),
            preserve_default=True,
        ),
    ]
