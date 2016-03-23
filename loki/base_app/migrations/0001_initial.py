# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('github_account', models.URLField(null=True, blank=True)),
                ('linkedin_account', models.URLField(null=True, blank=True)),
                ('twitter_account', models.URLField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('studies_at', models.CharField(max_length=110, null=True, blank=True)),
                ('works_at', models.CharField(max_length=110, null=True, blank=True)),
                ('avatar', models.ImageField(null=True, blank=True, upload_to='')),
                ('full_image', models.ImageField(null=True, blank=True, upload_to='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('logo_url', models.URLField(blank=True)),
                ('logo', models.ImageField(null=True, blank=True, upload_to='partners_logoes')),
                ('jobs_link', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('comapny', models.OneToOneField(primary_key=True, to='base_app.Company', serialize=False)),
                ('description', ckeditor.fields.RichTextField()),
                ('facebook', models.URLField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
                ('money_spent', models.PositiveIntegerField(default=0)),
                ('ordering', models.PositiveSmallIntegerField(default=0)),
                ('twitter', models.URLField(null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('video_presentation', models.URLField(null=True, blank=True)),
            ],
            options={
                'ordering': ('ordering',),
            },
        ),
        migrations.AddField(
            model_name='baseuser',
            name='birth_place',
            field=models.ForeignKey(blank=True, to='base_app.City', null=True),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', blank=True, to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', related_name='user_set'),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', blank=True, to='auth.Permission', help_text='Specific permissions for this user.', verbose_name='user permissions', related_name='user_set'),
        ),
        migrations.CreateModel(
            name='GeneralPartner',
            fields=[
                ('partner', models.OneToOneField(primary_key=True, to='base_app.Partner', serialize=False)),
            ],
        ),
    ]
