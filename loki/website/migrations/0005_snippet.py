# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20150808_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(unique=True, max_length=30)),
                ('text', ckeditor.fields.RichTextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
