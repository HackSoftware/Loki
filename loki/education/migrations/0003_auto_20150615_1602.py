# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_auto_20150613_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('description', models.URLField()),
                ('is_exam', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=128)),
                ('week', models.SmallIntegerField(default=1)),
                ('course', models.ForeignKey(to='education.Course')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('name', 'description')]),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='date',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
