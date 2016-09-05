from test_plus.test import TestCase
from ..models import Student

from loki.seed.factories import BaseUserFactory, StudentFactory


class TestManagers(TestCase):
    def test_create_from_baseuser_creates_new_student(self):
        base = BaseUserFactory()

        self.assertEqual(0, Student.objects.count())

        student = Student.objects.create_from_baseuser(base)

        self.assertEqual(1, Student.objects.count())
        self.assertEqual(base.pk, student.pk)

    def test_create_from_baseuser_for_existing_student_returns_none(self):
        student = StudentFactory()

        self.assertEqual(1, Student.objects.count())

        result = Student.objects.create_from_baseuser(student)

        self.assertIsNone(result)
        self.assertEqual(1, Student.objects.count())
