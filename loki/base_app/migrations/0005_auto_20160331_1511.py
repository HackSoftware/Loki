# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0004_faculty_abbreviation'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField()),
                ('place', models.ForeignKey(to='base_app.EducationPlace')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='baseuser',
            name='education_info',
            field=models.ManyToManyField(through='base_app.EducationInfo', to='base_app.EducationPlace'),
        ),
    ]
