# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import ckeditor.fields
import django_resized.forms
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', default=False, verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=75, unique=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('github_account', models.URLField(null=True, blank=True)),
                ('linkedin_account', models.URLField(null=True, blank=True)),
                ('twitter_account', models.URLField(null=True, blank=True)),
                ('studies_at', models.CharField(max_length='110', null=True, blank=True)),
                ('works_at', models.CharField(max_length='110', null=True, blank=True)),
                ('avatar', django_resized.forms.ResizedImageField(upload_to='avatar', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('baseuser_ptr', models.OneToOneField(primary_key=True, serialize=False, parent_link=True, to=settings.AUTH_USER_MODEL, auto_created=True)),
                ('is_vegetarian', models.BooleanField(default=False)),
                ('faculty_number', models.IntegerField(null=True)),
                ('shirt_size', models.SmallIntegerField(default=1, choices=[(1, 'S'), (2, 'M'), (3, 'L'), (4, 'XL')])),
                ('needs_work', models.BooleanField(default=True)),
                ('social_links', models.TextField(blank=True)),
                ('registered', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('hack_fmi.baseuser',),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('competitor', models.ForeignKey(to='hack_fmi.Competitor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField()),
                ('picture', models.ImageField(upload_to='', blank=True)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('capacity', models.SmallIntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('topic', models.CharField(max_length=100)),
                ('front_page', ckeditor.fields.RichTextField(blank=True)),
                ('min_team_members_count', models.SmallIntegerField(default=1)),
                ('max_team_members_count', models.SmallIntegerField(default=6)),
                ('sign_up_deadline', models.DateField()),
                ('make_team_dead_line', models.DateField()),
                ('mentor_pick_start_date', models.DateField()),
                ('mentor_pick_end_date', models.DateField()),
                ('max_mentor_pick', models.SmallIntegerField(default=1)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('idea_description', models.TextField()),
                ('repository', models.URLField(blank=True)),
                ('need_more_members', models.BooleanField(default=True)),
                ('members_needed_desc', models.CharField(max_length=255, blank=True)),
                ('picture', models.ImageField(upload_to='', blank=True)),
                ('place', models.SmallIntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamMembership',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('is_leader', models.BooleanField(default=False)),
                ('competitor', models.ForeignKey(to='hack_fmi.Competitor')),
                ('team', models.ForeignKey(to='hack_fmi.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(through='hack_fmi.TeamMembership', to='hack_fmi.Competitor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='mentors',
            field=models.ManyToManyField(blank=True, to='hack_fmi.Mentor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='room',
            field=models.ForeignKey(blank=True, null=True, to='hack_fmi.Room'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='season',
            field=models.ForeignKey(to='hack_fmi.Season', default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='team',
            name='technologies',
            field=models.ManyToManyField(blank=True, to='hack_fmi.Skill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='room',
            name='season',
            field=models.ForeignKey(to='hack_fmi.Season'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='partner',
            name='seasons',
            field=models.ManyToManyField(to='hack_fmi.Season'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mentor',
            name='from_company',
            field=models.ForeignKey(null=True, to='hack_fmi.Partner'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mentor',
            name='seasons',
            field=models.ManyToManyField(to='hack_fmi.Season'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='team',
            field=models.ForeignKey(to='hack_fmi.Team'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('team', 'competitor')]),
        ),
        migrations.AddField(
            model_name='competitor',
            name='known_skills',
            field=models.ManyToManyField(to='hack_fmi.Skill'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='baseuser',
            name='groups',
            field=models.ManyToManyField(related_name='user_set', blank=True, verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_query_name='user', to='auth.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='baseuser',
            name='user_permissions',
            field=models.ManyToManyField(related_name='user_set', blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.', related_query_name='user', to='auth.Permission'),
            preserve_default=True,
        ),
    ]
