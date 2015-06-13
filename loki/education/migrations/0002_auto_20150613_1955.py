# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import education.validators


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
                ('baseuser_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, to=settings.AUTH_USER_MODEL, parent_link=True)),
                ('mac', models.CharField(max_length=17, null=True, blank=True, validators=[education.validators.validate_mac])),
                ('phone', models.CharField(max_length='20', null=True, blank=True)),
                ('courses', models.ManyToManyField(through='education.CourseAssignment', to='education.Course')),
                ('hr_of', models.ForeignKey(null=True, to='base_app.Partner', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('hack_fmi.baseuser',),
        ),
        migrations.CreateModel(
            name='StudentNote',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
                ('baseuser_ptr', models.OneToOneField(primary_key=True, auto_created=True, serialize=False, to=settings.AUTH_USER_MODEL, parent_link=True)),
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
            field=models.ManyToManyField(null=True, to='base_app.Partner', blank=True),
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
            field=models.ManyToManyField(null=True, to='base_app.Partner', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='checkin',
            name='student',
            field=models.ForeignKey(null=True, to='education.Student', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='checkin',
            unique_together=set([('student', 'date'), ('mac', 'date')]),
        ),
    ]
