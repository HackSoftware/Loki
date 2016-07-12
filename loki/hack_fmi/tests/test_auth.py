from rest_framework.test import APIClient
from test_plus.test import TestCase
from django.core.urlresolvers import reverse

# from ..models import Skill

from seed import factories

from faker import Factory

faker = Factory.create()


class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.baseuser = factories.BaseUserFactory()

        self.baseuser.is_active = True
        self.baseuser.save()

    # def test_onboard_competitor_add_data_to_profile(self):
    #     self.client = APIClient()
    #     self.client.force_authenticate(user=self.user)
    #     url = reverse('hack_fmi:onboard_competitor')
    #     data = {
    #         'known_skills': [self.skill.id],
    #         'is_vegetarian': True,
    #         'shirt_size': 3,
    #         'needs_work': False,
    #         'social_links': "google.bg",
    #     }
    #     comp_count = Competitor.objects.count()
    #     base_count = BaseUser.objects.count()

    #     response = self.client.post(url, data, format='json')

    #     new_competitor = Competitor.objects.first()
    #     self.assertEqual(new_competitor.is_vegetarian, data['is_vegetarian'])
    #     self.assertEqual(new_competitor.shirt_size, data['shirt_size'])
    #     self.assertEqual(new_competitor.needs_work, data['needs_work'])
    #     self.assertEqual(new_competitor.known_skills.all()[0], self.skill)

    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(Competitor.objects.count(), comp_count+1)
    #     self.assertEqual(BaseUser.objects.count(), base_count)

    #     self.assertEqual(
    #         BaseUser.objects.first().email,
    #         Competitor.objects.first().email
    #     )

    def test_login_base_user(self):
        data = {
            'email': self.baseuser.email,
            'password': factories.BaseUserFactory.password,
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 206)

    def test_login_base_user_with_wrong_pass(self):
        data = {
            'email': self.baseuser.email,
            'password': faker.password(),
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)

    def test_login_competitor(self):
        competitor = factories.CompetitorFactory(
            baseuser_ptr_id=self.baseuser.id,
        )
        competitor.is_active = True
        # CompetitorFactory does not hash the parent password
        competitor.set_password(competitor.password)
        competitor.save()

        data = {
            'email': competitor.email,
            'password': factories.CompetitorFactory.password,
        }

        url = reverse('hack_fmi:login')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

    def test_login_competitor_with_wrong_pass(self):
        competitor = factories.CompetitorFactory(
            baseuser_ptr_id=self.baseuser.id,
        )
        competitor.is_active = True
        competitor.set_password(competitor.password)
        competitor.save()

        data = {
            'email': competitor.email,
            'password': faker.password(),
        }

        url = reverse('hack_fmi:login')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)

    def test_logout(self):
        self.client.force_authenticate(self.baseuser)

        url = reverse('hack_fmi:logout')
        response = self.client.post(url)

        self.response_200(response)
