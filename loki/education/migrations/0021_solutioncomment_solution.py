# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0020_solutioncomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='solutioncomment',
            name='solution',
            field=models.ForeignKey(null=True, to='education.Solution', blank=True),
            preserve_default=True,
        ),
    ]
