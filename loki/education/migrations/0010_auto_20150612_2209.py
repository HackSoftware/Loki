# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0009_auto_20150612_1725'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentNote',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('text', models.TextField(blank=True)),
                ('post_time', models.DateTimeField(auto_now=True)),
                ('assignment', models.ForeignKey(to='education.CourseAssignment')),
                ('author', models.ForeignKey(to='education.Teacher')),
            ],
            options={
                'ordering': ('post_time',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='course',
            field=models.ForeignKey(to='education.Course'),
            preserve_default=True,
        ),
    ]
