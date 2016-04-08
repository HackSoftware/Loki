# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0009_baseuserregistertoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuserregistertoken',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
