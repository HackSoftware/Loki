from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient

from ..models import Competitor, BaseUser, Skill


class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = BaseUser.objects.create(
            email="test@test.bg",
            first_name="Tester",
            last_name="Testov"
        )
        self.skill = Skill.objects.create(name='C#')

    def test_onboard_competitor_link_base_user(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('hack_fmi:onboard_competitor')
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Competitor.objects.count(), 1)
        self.assertEqual(BaseUser.objects.count(), 1)

        self.assertEqual(
            BaseUser.objects.first().email,
            Competitor.objects.first().email
        )

    def test_onboard_competitor_add_data_to_profile(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('hack_fmi:onboard_competitor')
        data = {
            'known_skills': self.skill.name,
            'is_vegetarian': True,
            'shirt_size': 3,
            'needs_work': False,
            'social_links': "google.bg",
        }
        self.client.post(url, data, format='json')

        new_competitor = Competitor.objects.first()
        self.assertEqual(new_competitor.is_vegetarian, data['is_vegetarian'])
        self.assertEqual(new_competitor.shirt_size, data['shirt_size'])
        self.assertEqual(new_competitor.needs_work, data['needs_work'])
        self.assertEqual(new_competitor.known_skills[0], data['known_skills'])
