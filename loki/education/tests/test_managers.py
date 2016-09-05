from test_plus.test import TestCase
from ..models import Student

from loki.seed.factories import BaseUserFactory


class TestManagers(TestCase):
    def test_create_from_baseuser_creates_new_student(self):
        base = BaseUserFactory()

        self.assertEqual(0, Student.objects.count())

        Student.objects.create_from_baseuser(base)

        self.assertEqual(1, Student.objects.count())
