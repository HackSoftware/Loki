# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-05 10:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('website', '0003_coursedescription_video'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('skype', models.CharField(blank=True, max_length=255, null=True)),
                ('works_at', models.CharField(blank=True, max_length=255, null=True)),
                ('studies_at', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('course', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='website.CourseDescription')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationProblem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description_url', models.URLField(blank=True, null=True)),
                ('application_info', models.ManyToManyField(to='applications.ApplicationInfo')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationProblemSolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution_url', models.URLField(blank=True, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applications.Application')),
                ('problem', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='applications.ApplicationProblem')),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='application_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applications.ApplicationInfo'),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='application',
            unique_together=set([('application_info', 'user')]),
        ),
    ]
