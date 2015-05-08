# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_conf', '0004_auto_20150508_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='description',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='speaker',
            name='facebook',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='speaker',
            name='github',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='speaker',
            name='google_plus',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='speaker',
            name='picture',
            field=models.ImageField(blank=True, upload_to=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='speaker',
            name='title',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='speaker',
            name='twitter',
            field=models.URLField(blank=True),
            preserve_default=True,
        ),
    ]
