# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('baseuser_ptr', models.OneToOneField(parent_link=True, primary_key=True, serialize=False, auto_created=True, to=settings.AUTH_USER_MODEL)),
                ('is_vegetarian', models.BooleanField(default=False)),
                ('faculty_number', models.IntegerField(null=True)),
                ('shirt_size', models.SmallIntegerField(choices=[(1, 'S'), (2, 'M'), (3, 'L'), (4, 'XL')], default=1)),
                ('needs_work', models.BooleanField(default=True)),
                ('social_links', models.TextField(blank=True)),
                ('registered', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('base_app.baseuser',),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('competitor', models.ForeignKey(to='hack_fmi.Competitor')),
            ],
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField()),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('number', models.IntegerField()),
                ('capacity', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
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
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('idea_description', models.TextField()),
                ('repository', models.URLField(blank=True)),
                ('need_more_members', models.BooleanField(default=True)),
                ('members_needed_desc', models.CharField(max_length=255, blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('place', models.SmallIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMembership',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('is_leader', models.BooleanField(default=False)),
                ('competitor', models.ForeignKey(to='hack_fmi.Competitor')),
                ('team', models.ForeignKey(to='hack_fmi.Team')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(through='hack_fmi.TeamMembership', to='hack_fmi.Competitor'),
        ),
        migrations.AddField(
            model_name='team',
            name='mentors',
            field=models.ManyToManyField(blank=True, to='hack_fmi.Mentor'),
        ),
        migrations.AddField(
            model_name='team',
            name='room',
            field=models.ForeignKey(blank=True, to='hack_fmi.Room', null=True),
        ),
        migrations.AddField(
            model_name='team',
            name='season',
            field=models.ForeignKey(to='hack_fmi.Season', default=1),
        ),
        migrations.AddField(
            model_name='team',
            name='technologies',
            field=models.ManyToManyField(blank=True, to='hack_fmi.Skill'),
        ),
        migrations.AddField(
            model_name='room',
            name='season',
            field=models.ForeignKey(to='hack_fmi.Season'),
        ),
        migrations.AddField(
            model_name='partner',
            name='seasons',
            field=models.ManyToManyField(to='hack_fmi.Season'),
        ),
        migrations.AddField(
            model_name='mentor',
            name='from_company',
            field=models.ForeignKey(to='hack_fmi.Partner', null=True),
        ),
        migrations.AddField(
            model_name='mentor',
            name='seasons',
            field=models.ManyToManyField(to='hack_fmi.Season'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='team',
            field=models.ForeignKey(to='hack_fmi.Team'),
        ),
        migrations.AddField(
            model_name='competitor',
            name='known_skills',
            field=models.ManyToManyField(to='hack_fmi.Skill'),
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('team', 'competitor')]),
        ),
    ]
