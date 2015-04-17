# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0029_auto_20150416_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='front_page',
            field=ckeditor.fields.RichTextField(blank=True),
            preserve_default=True,
        ),
    ]
