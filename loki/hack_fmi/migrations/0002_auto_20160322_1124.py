# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', to='auth.Group', verbose_name='groups', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='last_login',
            field=models.DateTimeField(null=True, blank=True, verbose_name='last login'),
        ),
    ]
