# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20151007_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursedescription',
            name='application_deadline',
        ),
        migrations.RemoveField(
            model_name='coursedescription',
            name='github',
        ),
        migrations.RemoveField(
            model_name='coursedescription',
            name='video_url',
        ),
        migrations.AddField(
            model_name='coursedescription',
            name='course_days',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursedescription',
            name='course_intensity',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
