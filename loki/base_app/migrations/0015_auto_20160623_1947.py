# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0014_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partner',
            old_name='comapny',
            new_name='company',
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='education_info',
            field=models.ManyToManyField(through='base_app.EducationInfo', to='base_app.EducationPlace', related_name='info'),
        ),
        migrations.AlterField(
            model_name='educationinfo',
            name='faculty',
            field=models.ForeignKey(related_name='related_fac_to_user', to='base_app.Faculty', blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='educationinfo',
            name='subject',
            field=models.ForeignKey(related_name='related_subj_to_user', to='base_app.Subject', blank=True, null=True),
        ),
    ]
