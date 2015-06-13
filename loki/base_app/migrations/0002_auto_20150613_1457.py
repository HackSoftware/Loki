# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='id',
        ),
        migrations.AddField(
            model_name='partner',
            name='comapny',
            field=models.OneToOneField(primary_key=True, default=1, serialize=False, to='base_app.Company'),
            preserve_default=False,
        ),
    ]
