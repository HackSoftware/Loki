# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='successstoryperson',
            name='show_picture_on_site',
            field=models.BooleanField(default=True),
        ),
    ]
