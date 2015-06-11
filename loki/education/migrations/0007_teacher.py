# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import education.validators


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0049_auto_20150611_1336'),
        ('education', '0006_auto_20150611_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('baseuser_ptr', models.OneToOneField(parent_link=True, primary_key=True, auto_created=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('mac', models.CharField(max_length=17, blank=True, validators=[education.validators.validate_mac], null=True)),
                ('phone', models.CharField(max_length='20', blank=True, null=True)),
                ('teached_courses', models.ManyToManyField(to='education.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=('hack_fmi.baseuser',),
        ),
    ]
