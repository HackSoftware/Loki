from django.core.management import call_command
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient

from education.models import Student, CheckIn
from hack_fmi.models import BaseUser
from loki.settings import CHECKIN_TOKEN


class CheckInTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12-34-56-78-9A-BC",
        )
        self.student_no_mac = Student.objects.create(
            email='rado@abv.bg',
        )

    def test_check_in_with_mac_and_user(self):
        data = {
            'mac': '12-34-56-78-9A-BC',
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        self.client.post(url, data, format='json')
        self.assertIn(self.student.mac, CheckIn.objects.first().student.mac)

    def test_check_in_with_mac_and_no_user(self):
        data = {
            'mac': '12-34-56-78-9A-BA',
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.client.post(url, data, format='json')

    def test_check_macs_command(self):
        data = {
            'mac': '12-34-56-78-9A-BA',
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        self.client.post(url, data, format='json')
        self.assertIsNone(CheckIn.objects.first().student)
        self.student_no_mac.mac = '12-34-56-78-9A-BA'
        self.student_no_mac.save()
        call_command('check_macs')
        self.assertEqual(CheckIn.objects.first().student, self.student_no_mac)


class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = BaseUser.objects.create(
            email="test@test.bg",
            first_name="Tester",
            last_name="Testov"
        )

    def test_onboard_student(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('education:onboard_student')
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(BaseUser.objects.count(), 1)

        self.assertEqual(
            BaseUser.objects.first().email,
            Student.objects.first().email
        )
