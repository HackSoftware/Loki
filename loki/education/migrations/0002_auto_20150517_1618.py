# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('mac', models.CharField(max_length=17)),
                ('date', models.DateField(auto_now=True)),
                ('student', models.ForeignKey(null=True, to='education.Student', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='checkin',
            unique_together=set([('student', 'date')]),
        ),
    ]
