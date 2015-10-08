# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_coursedescription_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedescription',
            name='logo',
            field=models.CharField(max_length=255, blank=True, help_text='Add class from <a href="http://devicon.fr/" target="_blank">www.devicon.fr</a>'),
            preserve_default=True,
        ),
    ]
