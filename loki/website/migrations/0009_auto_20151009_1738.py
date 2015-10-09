# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_auto_20151009_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursedescription',
            name='address',
            field=models.CharField(blank=True, help_text='Add <a href="http://www.google.com/maps" target="_blank">google maps</a>link to HackBulgaria location', max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursedescription',
            name='teacher_preview',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
