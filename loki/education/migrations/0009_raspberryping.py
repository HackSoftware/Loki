# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0008_courseassignment_student_presence'),
    ]

    operations = [
        migrations.CreateModel(
            name='RaspberryPing',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=10, default='ping')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
