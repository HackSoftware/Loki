# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20151008_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedescription',
            name='logo',
            field=models.CharField(max_length=255, blank=True, help_text='Copy class from <a href="http://devicon.fr/" target="_blank">www.devicon.fr</a>'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='coursedescription',
            name='video_image',
            field=models.ImageField(upload_to='', blank=True, help_text='Add a 16/9 video cover image.'),
            preserve_default=True,
        ),
    ]
