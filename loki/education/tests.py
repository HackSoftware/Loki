from django.test import TestCase
from education.models import Student, CheckIn
from django.core.urlresolvers import reverse


class CheckInTest(TestCase):
    """Set token in your local_settings to 123"""

    def setUp(self):
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12-34-56-78-9A-BC",
        )

    def test_check_in_with_mac_and_user(self):

        data = {
            'mac': '12-34-56-78-9A-BC',
            'token': '123',
        }
        url = reverse('education:set_check_in')
        self.client.post(url, data, format='json')
        self.assertIn(self.student.mac, CheckIn.objects.first().student.mac)

    def test_check_in_with_mac_and_no_user(self):
        data = {
            'mac': '12-34-56-78-9A-BA',
            'token': '123',
        }
        url = reverse('education:set_check_in')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.client.post(url, data, format='json')
