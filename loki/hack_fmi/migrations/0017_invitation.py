# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hack_fmi', '0016_auto_20150331_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('competitor', models.ForeignKey(to='hack_fmi.Competitor')),
                ('team', models.ForeignKey(to='hack_fmi.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
