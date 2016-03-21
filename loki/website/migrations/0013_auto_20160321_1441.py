# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_auto_20160203_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursedescription',
            name='custom_logo',
            field=models.ImageField(upload_to='', help_text='Add a custom course logo with 308x308 size.', blank=True),
            preserve_default=True,
        ),
    ]
