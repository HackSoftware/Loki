# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BinaryFileTest',
            fields=[
                ('test_ptr', models.OneToOneField(serialize=False, to='education.Test', primary_key=True, auto_created=True, parent_link=True)),
                ('file', models.FileField(upload_to='/media/tests')),
            ],
            bases=('education.test',),
        ),
        migrations.CreateModel(
            name='SourceCodeTest',
            fields=[
                ('test_ptr', models.OneToOneField(serialize=False, to='education.Test', primary_key=True, auto_created=True, parent_link=True)),
                ('sourcecode', models.TextField(blank=True, null=True)),
            ],
            bases=('education.test',),
        ),
        migrations.RemoveField(
            model_name='test',
            name='github_url',
        ),
    ]
