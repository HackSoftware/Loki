# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EducationPlace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=1000, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=1000, unique=True)),
                ('faculty', models.ForeignKey(to='base_app.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Academy',
            fields=[
                ('educationplace_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='base_app.EducationPlace', serialize=False, primary_key=True)),
            ],
            bases=('base_app.educationplace',),
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('educationplace_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='base_app.EducationPlace', serialize=False, primary_key=True)),
            ],
            bases=('base_app.educationplace',),
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('educationplace_ptr', models.OneToOneField(auto_created=True, parent_link=True, to='base_app.EducationPlace', serialize=False, primary_key=True)),
            ],
            bases=('base_app.educationplace',),
        ),
        migrations.AddField(
            model_name='educationplace',
            name='city',
            field=models.ForeignKey(to='base_app.City'),
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together=set([('faculty', 'name')]),
        ),
        migrations.AddField(
            model_name='faculty',
            name='uni',
            field=models.ForeignKey(to='base_app.University'),
        ),
        migrations.AlterUniqueTogether(
            name='faculty',
            unique_together=set([('uni', 'name')]),
        ),
    ]
