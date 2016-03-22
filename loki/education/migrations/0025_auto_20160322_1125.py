# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


def gen_uuid(apps, schema_editor):
    Certificate = apps.get_model('education', 'Certificate')
    for row in Certificate.objects.all():
        row.token = uuid.uuid4()
        row.save()


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0024_certificate_token'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
