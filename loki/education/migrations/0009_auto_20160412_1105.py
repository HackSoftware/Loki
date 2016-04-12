# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0008_test_extra_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='extra_options',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
    ]
