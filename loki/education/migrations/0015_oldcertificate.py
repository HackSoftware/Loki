# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0014_auto_20150714_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldCertificate',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('url_id', models.PositiveIntegerField()),
                ('assignment', models.ForeignKey(to='education.CourseAssignment')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
