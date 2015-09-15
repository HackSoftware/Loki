# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='author',
            new_name='speaker',
        ),
        migrations.AddField(
            model_name='schedule',
            name='co_speaker',
            field=models.ForeignKey(related_name='co_schedule', to='hack_conf.Speaker', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='title',
            field=models.SmallIntegerField(choices=[(1, 'Sponsor'), (2, 'General Media Partner'), (3, 'Branch Partner'), (4, 'Media Partner'), (5, 'School Partner'), (6, 'Silver Sponsor'), (7, 'Gold Sponsor'), (8, 'Platinum Sponsor')], default=1),
            preserve_default=True,
        ),
    ]
