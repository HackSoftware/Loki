# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0020_course_generate_certificates_until'),
    ]

    operations = [
        migrations.RenameModel('OldCertificate', 'Certificate')
    ]
