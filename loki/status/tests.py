import unittest

from django.core.urlresolvers import reverse
from django.test import TestCase

from education.models import CheckIn, Student


"""
TODO: Check what is happening here.
unskip when sure
"""


@unittest.skip
class SanityCheckerTest(TestCase):

    def test_no_check_ins_today(self):
        url = reverse('status:check_raspberry')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_one_check_in_today(self):
        self.student = Student.objects.create(
            email="stud@abv.bg",
            mac="60:67:20:cc:b1:62"
        )
        CheckIn.objects.create(
            mac="12-34-56-78-9A-BE",
            student=self.student,
        )
        url = reverse('status:check_raspberry')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
