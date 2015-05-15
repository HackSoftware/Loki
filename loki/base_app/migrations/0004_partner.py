# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0003_auto_20150504_1517'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('description', ckeditor.fields.RichTextField()),
                ('facebook', models.URLField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('logo', models.ImageField(upload_to='partner_logoes', blank=True, null=True)),
                ('money_spent', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=128)),
                ('ordering', models.PositiveSmallIntegerField(default=0)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ('ordering',),
            },
            bases=(models.Model,),
        ),
    ]
