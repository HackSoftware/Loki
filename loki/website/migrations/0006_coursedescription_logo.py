# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_remove_coursedescription_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursedescription',
            name='logo',
            field=models.CharField(max_length=255, help_text='Add icon class', blank=True),
            preserve_default=True,
        ),
    ]
