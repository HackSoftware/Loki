from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Skill, Competitor, BaseUser, TeamMembership
from django.core import mail


class RegistrationTests(APITestCase):
    def setUp(self):
        self.skills = Skill.objects.create(name="C#")

    def test_register_user(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': 'Bachvarov',
            'faculty_number': '123',
            'known_skills': '1',
            'password': '123'
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competitor.objects.count(), 1)
        self.assertEqual(BaseUser.objects.count(), 1)

    def test_registraion_full_name(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': 'Bachvarov',
            'faculty_number': '123',
            'known_skills': '1',
            'password': '123'
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_no_password(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': 'Bachvarov',
            'faculty_number': '123',
            'known_skills': '1',
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_sent(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': ' Bachvarov',
            'faculty_number': '123',
            'known_skills': '1',
            'password': '123'
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)


class LoginTests(APITestCase):
    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        self.competitor = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )
        self.competitor.set_password('123')
        self.competitor.is_active = True
        self.competitor.save()

    def test_login(self):
        data = {
            'email': 'ivo@abv.bg',
            'password': '123',
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_password(self):
        data = {
            'email': 'ivo@abv.bg',
            'password': '123321',
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_not_competetor(self):
        self.baseuser = BaseUser.objects.create(
            email='baseuser@abv.bg',
            full_name='Ivo Naidobriq',
        )
        self.baseuser.set_password('123')
        self.baseuser.save()

        data = {
            'email': 'baseuser@abv.bg',
            'password': '123',
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_data_after_login(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor)
        url = reverse('hack_fmi:me')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.competitor.email)

    def test_get_data_not_login(self):
        url = reverse('hack_fmi:me')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TeamRegistrationTests(APITestCase):
    def setUp(self):
        self.skills = Skill.objects.create(name="C#")
        self.competitor = Competitor.objects.create(
            email='ivo@abv.bg',
            full_name='Ivo Naidobriq',
            faculty_number='123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor)

    def test_register_team(self):
        data = {
            'name': 'Pandas',
            'idea_description': 'GameDevelopers',
            'repository': 'https://github.com/HackSoftware',
            'technologies': 1,
        }
        url = reverse('hack_fmi:register_team')
        response = self.client.post(url, data, format='json')

        self.assertEqual(len(response.data['members']), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(len(response.data['technologies']), 1)

    def test_registered_team_has_leader(self):
        data = {
            'name': 'Pandas',
            'idea_description': 'GameDevelopers',
            'repository': 'https://github.com/HackSoftware',
            'technologies': 1,
        }
        url = reverse('hack_fmi:register_team')
        self.client.post(url, data, format='json')
        team_membership = TeamMembership.objects.get(id=1)
        self.assertEqual(self.competitor, team_membership.competitor)
        self.assertTrue(team_membership.is_leader)
        url = reverse('hack_fmi:me')
