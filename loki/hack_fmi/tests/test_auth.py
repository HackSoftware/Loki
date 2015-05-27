from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework.test import APIClient

from ..models import Competitor, BaseUser, Skill


class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = BaseUser.objects.create_user(
            email="test@test.bg",
            password="123",
            full_name='Test Testov'
        )
        self.user.is_active = True
        self.user.save()
        self.competitor = BaseUser.objects.create_user(
            email="comp@comp.bg",
            password="123",
            full_name='Comp compov'
        )
        self.competitor.is_active = True
        self.competitor.make_competitor()
        self.competitor.save()
        self.skill = Skill.objects.create(name='C#')

    def test_onboard_competitor_add_data_to_profile(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('hack_fmi:onboard_competitor')
        data = {
            'known_skills': [self.skill.id],
            'is_vegetarian': True,
            'shirt_size': 3,
            'needs_work': False,
            'social_links': "google.bg",
        }
        comp_count = Competitor.objects.count()
        base_count = BaseUser.objects.count()

        response = self.client.post(url, data, format='json')

        new_competitor = Competitor.objects.first()
        self.assertEqual(new_competitor.is_vegetarian, data['is_vegetarian'])
        self.assertEqual(new_competitor.shirt_size, data['shirt_size'])
        self.assertEqual(new_competitor.needs_work, data['needs_work'])
        self.assertEqual(new_competitor.known_skills.all()[0], self.skill)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Competitor.objects.count(), comp_count+1)
        self.assertEqual(BaseUser.objects.count(), base_count)

        self.assertEqual(
            BaseUser.objects.first().email,
            Competitor.objects.first().email
        )

    def test_login_base_user(self):
        data = {
            'password': '123',
            'email': 'test@test.bg'
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        print(response.status_code)

    def test_login_competitor(self):
        data = {
            'password': '123',
            'email': 'comp@comp.bg'
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
