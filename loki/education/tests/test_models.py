from test_plus.test import TestCase
from django.core.exceptions import ValidationError

from loki.seed.factories import StudentFactory
from loki.education.models import WorkingAt
from loki.base_app.models import Company
from datetime import datetime

class WorkingAtTest(TestCase):

    def test_saving_workingat_with_both_company_and_company_name(self):
        company = Company.objects.create(name="Hack")
        with self.assertRaises(ValidationError):
            WorkingAt.objects.create(start_date=datetime.now().date())
        self.assertEqual(0, WorkingAt.objects.all().count())

    def test_saving_working_at_with_only_company(self):
        company = Company.objects.create(name="Hack")
        student = StudentFactory()
        WorkingAt.objects.create(company=company, student=student, start_date=datetime.now().date())
        self.assertEqual(1, WorkingAt.objects.all().count())

    def test_saving_working_at_with_company_name(self):
        student = StudentFactory()
        WorkingAt.objects.create(company_name="Hack", student=student, start_date=datetime.now().date())
        self.assertEqual(1, WorkingAt.objects.all().count())
