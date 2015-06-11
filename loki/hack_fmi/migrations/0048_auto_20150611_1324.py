# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0047_baseuser_twitter_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='studies_at1',
            field=models.CharField(max_length='110', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='baseuser',
            name='works_at1',
            field=models.CharField(max_length='110', null=True, blank=True),
            preserve_default=True,
        ),
    ]
