# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0003_generalpartner'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='base_user',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='event',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
