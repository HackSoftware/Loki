# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import education.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0001_initial'),
        ('base_app', '0001_initial'),
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('baseuser_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to=settings.AUTH_USER_MODEL, auto_created=True)),
                ('status', models.SmallIntegerField(default=1, choices=[(1, 'Student'), (2, 'HR'), (3, 'Teacher')])),
                ('mac', models.CharField(max_length=17, null=True, blank=True, validators=[education.validators.validate_mac])),
                ('phone', models.CharField(max_length='20', null=True, blank=True)),
                ('courses', models.ManyToManyField(through='education.CourseAssignment', to='education.Course')),
                ('hr_of', models.ForeignKey(blank=True, null=True, to='base_app.Partner')),
            ],
            options={
                'abstract': False,
            },
            bases=('hack_fmi.baseuser',),
        ),
        migrations.CreateModel(
            name='StudentNote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('post_time', models.DateTimeField(auto_now=True)),
                ('assignment', models.ForeignKey(to='education.CourseAssignment')),
            ],
            options={
                'ordering': ('post_time',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('baseuser_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to=settings.AUTH_USER_MODEL, auto_created=True)),
                ('mac', models.CharField(max_length=17, null=True, blank=True, validators=[education.validators.validate_mac])),
                ('phone', models.CharField(max_length='20', null=True, blank=True)),
                ('teached_courses', models.ManyToManyField(to='education.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=('hack_fmi.baseuser',),
        ),
        migrations.AddField(
            model_name='studentnote',
            name='author',
            field=models.ForeignKey(to='education.Teacher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='lecture',
            name='course',
            field=models.ForeignKey(to='education.Course'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='courseassignment',
            name='course',
            field=models.ForeignKey(to='education.Course'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='courseassignment',
            name='favourite_partners',
            field=models.ManyToManyField(null=True, blank=True, to='base_app.Partner'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='courseassignment',
            name='user',
            field=models.ForeignKey(to='education.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='course',
            name='partner',
            field=models.ManyToManyField(null=True, blank=True, to='base_app.Partner'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='checkin',
            name='student',
            field=models.ForeignKey(blank=True, null=True, to='education.Student'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='checkin',
            unique_together=set([('student', 'date'), ('mac', 'date')]),
        ),
    ]
