# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('hack_fmi', '0033_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=60)),
                ('seasons', models.ManyToManyField(to='hack_fmi.Season')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', to='auth.Group', related_query_name='user', related_name='user_set', verbose_name='groups', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='baseuser',
            name='is_superuser',
            field=models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='baseuser',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Specific permissions for this user.', to='auth.Permission', related_query_name='user', related_name='user_set', verbose_name='user permissions', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='competitor',
            name='registered',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mentor',
            name='from_company',
            field=models.ForeignKey(to='hack_fmi.Partner', default='', blank=True),
            preserve_default=False,
        ),
    ]
