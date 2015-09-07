# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='base_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticket',
            name='event',
            field=models.ForeignKey(to='base_app.Event'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set([('event', 'base_user')]),
        ),
    ]
