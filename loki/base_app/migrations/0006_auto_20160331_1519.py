# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0005_auto_20160331_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationinfo',
            name='faculty',
            field=models.ForeignKey(to='base_app.Faculty', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='educationinfo',
            name='subject',
            field=models.ForeignKey(to='base_app.Subject', blank=True, null=True),
        ),
    ]
