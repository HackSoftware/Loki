# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_coursedescription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursedescription',
            old_name='video',
            new_name='video_url',
        ),
        migrations.RemoveField(
            model_name='coursedescription',
            name='description',
        ),
        migrations.RemoveField(
            model_name='coursedescription',
            name='short_description',
        ),
        migrations.AddField(
            model_name='coursedescription',
            name='application_deadline',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursedescription',
            name='course_summary',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursedescription',
            name='github',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursedescription',
            name='price',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursedescription',
            name='realization',
            field=ckeditor.fields.RichTextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursedescription',
            name='title',
            field=models.CharField(blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coursedescription',
            name='video_image',
            field=models.ImageField(blank=True, upload_to=''),
            preserve_default=True,
        ),
    ]
