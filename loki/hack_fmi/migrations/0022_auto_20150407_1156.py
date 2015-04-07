# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0021_mentor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='description',
            field=ckeditor.fields.RichTextField(),
            preserve_default=True,
        ),
    ]
