# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0021_auto_20150826_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='url_id',
        ),
    ]
