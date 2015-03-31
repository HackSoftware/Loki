# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0017_invitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='social_links',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
