# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0008_auto_20160103_1921'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraderRequest',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('request_info', models.CharField(max_length=140)),
                ('nonce', models.BigIntegerField(db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
