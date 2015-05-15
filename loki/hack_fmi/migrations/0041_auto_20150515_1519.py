# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0040_team_place'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='avatar',
            field=django_resized.forms.ResizedImageField(upload_to='avatar', blank=True),
            preserve_default=True,
        ),
    ]
