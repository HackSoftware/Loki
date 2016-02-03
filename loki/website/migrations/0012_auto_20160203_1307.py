# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_coursedescription_blog_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursedescription',
            name='custom_logo',
            field=models.ImageField(help_text='Add a custom cover image.', blank=True, upload_to=''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursedescription',
            name='paid_course',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
