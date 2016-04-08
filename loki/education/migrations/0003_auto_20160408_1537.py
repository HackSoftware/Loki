# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_test_info(apps, schema_editor):
    Test = apps.get_model('education', 'Test')
    SourceCodeTest = apps.get_model('education', 'SourceCodeTest')

    tests = Test.objects.all()
    for test in tests:
        SourceCodeTest.objects.create(
            task=test.task,
            language=test.language,
            test_type=test.test_type,
            sourcecode=test.code
        )
        test.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_auto_20160408_1536'),
    ]

    operations = [
        migrations.RunPython(migrate_test_info, reverse_code=migrations.RunPython.noop)
    ]
