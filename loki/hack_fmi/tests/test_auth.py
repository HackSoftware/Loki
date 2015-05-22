from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient

from ..models import Competitor, BaseUser


class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = BaseUser.objects.create(
            email="test@test.bg",
            first_name="Tester",
            last_name="Testov"
        )

    def test_onboard_competitor(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('hack_fmi:onboard_competitor')
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Competitor.objects.count(), 1)
        self.assertEqual(BaseUser.objects.count(), 1)

        self.assertEqual(
            BaseUser.objects.first().email,
            Competitor.objects.first().email
        )
