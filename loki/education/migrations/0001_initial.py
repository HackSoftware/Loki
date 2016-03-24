# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import ckeditor.fields
from django.conf import settings
import education.validators


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('token', models.CharField(default=uuid.uuid4, max_length=110, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('mac', models.CharField(max_length=17)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('description', ckeditor.fields.RichTextField()),
                ('git_repository', models.CharField(blank=True, max_length=256)),
                ('image', models.ImageField(blank=True, null=True, upload_to='courses_logoes')),
                ('name', models.CharField(max_length=64)),
                ('short_description', models.CharField(blank=True, max_length=300)),
                ('show_on_index', models.BooleanField(default=False)),
                ('is_free', models.BooleanField(default=True)),
                ('application_until', models.DateField()),
                ('applications_url', models.URLField(blank=True, null=True)),
                ('ask_for_favorite_partner', models.BooleanField(default=False)),
                ('ask_for_feedback', models.BooleanField(default=False)),
                ('end_time', models.DateField(blank=True, null=True)),
                ('fb_group', models.URLField(blank=True, null=True)),
                ('next_season_mail_list', models.URLField(blank=True, null=True)),
                ('SEO_description', models.CharField(max_length=255)),
                ('SEO_title', models.CharField(max_length=255)),
                ('start_time', models.DateField(blank=True, null=True)),
                ('url', models.SlugField(max_length=80, unique=True)),
                ('video', models.URLField(blank=True)),
                ('generate_certificates_until', models.DateField()),
                ('partner', models.ManyToManyField(blank=True, null=True, to='base_app.Partner')),
            ],
        ),
        migrations.CreateModel(
            name='CourseAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('cv', models.FileField(blank=True, null=True, upload_to='cvs')),
                ('group_time', models.SmallIntegerField(choices=[(1, 'Early'), (2, 'Late')])),
                ('is_attending', models.BooleanField(default=True)),
                ('student_presence', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('is_online', models.BooleanField(default=False)),
                ('course', models.ForeignKey(to='education.Course')),
                ('favourite_partners', models.ManyToManyField(blank=True, null=True, to='base_app.Partner')),
            ],
        ),
        migrations.CreateModel(
            name='GraderRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('request_info', models.CharField(max_length=140)),
                ('nonce', models.BigIntegerField(db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('date', models.DateField()),
                ('course', models.ForeignKey(to='education.Course')),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammingLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=110)),
            ],
        ),
        migrations.CreateModel(
            name='RetestSolution',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.SmallIntegerField(default=0, choices=[(0, 'pending'), (1, 'done')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('test_id', models.IntegerField()),
                ('tested_solutions_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('code', models.TextField(blank=True, null=True)),
                ('build_id', models.IntegerField(blank=True, null=True)),
                ('check_status_location', models.CharField(blank=True, max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.SmallIntegerField(default=6, choices=[(0, 'pending'), (1, 'running'), (2, 'ok'), (3, 'not_ok'), (4, 'submitted'), (5, 'missing'), (6, 'submitted_without_grading')])),
                ('test_output', models.TextField(blank=True, null=True)),
                ('return_code', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('baseuser_ptr', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, parent_link=True, serialize=False, auto_created=True)),
                ('mac', models.CharField(blank=True, max_length=17, validators=[education.validators.validate_mac], null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('skype', models.CharField(blank=True, max_length=20, null=True)),
                ('courses', models.ManyToManyField(through='education.CourseAssignment', to='education.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=('base_app.baseuser',),
        ),
        migrations.CreateModel(
            name='StudentNote',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('text', models.TextField(blank=True)),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(to='education.CourseAssignment')),
            ],
            options={
                'ordering': ('post_time',),
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('description', models.URLField()),
                ('is_exam', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=128)),
                ('week', models.SmallIntegerField(default=1)),
                ('gradable', models.BooleanField(default=True)),
                ('course', models.ForeignKey(to='education.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('baseuser_ptr', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, parent_link=True, serialize=False, auto_created=True)),
                ('mac', models.CharField(blank=True, max_length=17, validators=[education.validators.validate_mac], null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('signature', models.ImageField(blank=True, null=True, upload_to='teachers_signatures')),
                ('teached_courses', models.ManyToManyField(to='education.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=('base_app.baseuser',),
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('code', models.TextField(blank=True, null=True)),
                ('github_url', models.URLField()),
                ('test_type', models.SmallIntegerField(default=0, choices=[(0, 'unittest')])),
                ('language', models.ForeignKey(to='education.ProgrammingLanguage')),
                ('task', models.OneToOneField(to='education.Task')),
            ],
        ),
        migrations.CreateModel(
            name='WorkingAt',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('came_working', models.BooleanField(default=False)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('company', models.ForeignKey(null=True, to='base_app.Company', blank=True)),
                ('course', models.ForeignKey(null=True, to='education.Course', blank=True)),
                ('location', models.ForeignKey(to='base_app.City')),
                ('student', models.ForeignKey(to='education.Student')),
            ],
        ),
        migrations.AddField(
            model_name='studentnote',
            name='author',
            field=models.ForeignKey(to='education.Teacher'),
        ),
        migrations.AddField(
            model_name='solution',
            name='student',
            field=models.ForeignKey(to='education.Student'),
        ),
        migrations.AddField(
            model_name='solution',
            name='task',
            field=models.ForeignKey(to='education.Task'),
        ),
        migrations.AddField(
            model_name='courseassignment',
            name='user',
            field=models.ForeignKey(to='education.Student'),
        ),
        migrations.AddField(
            model_name='checkin',
            name='student',
            field=models.ForeignKey(null=True, to='education.Student', blank=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='assignment',
            field=models.OneToOneField(to='education.CourseAssignment'),
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together=set([('name', 'description')]),
        ),
        migrations.AlterUniqueTogether(
            name='courseassignment',
            unique_together=set([('user', 'course')]),
        ),
        migrations.AlterUniqueTogether(
            name='checkin',
            unique_together=set([('student', 'date'), ('mac', 'date')]),
        ),
    ]
