# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import education.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0001_initial'),
        ('education', '0001_initial'),
        ('base_app', '0002_auto_20150907_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('baseuser_ptr', models.OneToOneField(serialize=False, primary_key=True, parent_link=True, to=settings.AUTH_USER_MODEL, auto_created=True)),
                ('mac', models.CharField(null=True, blank=True, max_length=17, validators=[education.validators.validate_mac])),
                ('phone', models.CharField(null=True, blank=True, max_length='20')),
                ('courses', models.ManyToManyField(through='education.CourseAssignment', to='education.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=('hack_fmi.baseuser',),
        ),
        migrations.CreateModel(
            name='StudentNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(to='education.CourseAssignment')),
            ],
            options={
                'ordering': ('post_time',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('baseuser_ptr', models.OneToOneField(serialize=False, primary_key=True, parent_link=True, to=settings.AUTH_USER_MODEL, auto_created=True)),
                ('mac', models.CharField(null=True, blank=True, max_length=17, validators=[education.validators.validate_mac])),
                ('phone', models.CharField(null=True, blank=True, max_length='20')),
                ('teached_courses', models.ManyToManyField(to='education.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=('hack_fmi.baseuser',),
        ),
        migrations.CreateModel(
            name='WorkingAt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('came_working', models.BooleanField(default=False)),
                ('company_name', models.CharField(null=True, blank=True, max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True, blank=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(null=True, blank=True)),
                ('company', models.ForeignKey(null=True, blank=True, to='base_app.Company')),
                ('course', models.ForeignKey(null=True, blank=True, to='education.Course')),
                ('location', models.ForeignKey(to='base_app.City')),
                ('student', models.ForeignKey(to='education.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('name', 'description')]),
        ),
        migrations.AddField(
            model_name='studentnote',
            name='author',
            field=models.ForeignKey(to='education.Teacher'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='solution',
            name='student',
            field=models.ForeignKey(to='education.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='solution',
            name='task',
            field=models.ForeignKey(to='education.Task'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='solution',
            unique_together=set([('student', 'task')]),
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
        migrations.AlterUniqueTogether(
            name='courseassignment',
            unique_together=set([('user', 'course')]),
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
            field=models.ForeignKey(null=True, blank=True, to='education.Student'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='checkin',
            unique_together=set([('student', 'date'), ('mac', 'date')]),
        ),
        migrations.AddField(
            model_name='certificate',
            name='assignment',
            field=models.OneToOneField(to='education.CourseAssignment'),
            preserve_default=True,
        ),
    ]
