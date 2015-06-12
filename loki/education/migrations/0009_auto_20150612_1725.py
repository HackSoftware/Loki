# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0008_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='date',
            field=models.DateField(),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='checkin',
            unique_together=set([('student', 'date'), ('mac', 'date')]),
        ),
    ]
