from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Language, Competitor, BaseUser


class RegistrationTests(APITestCase):
    def setUp(self):
        self.language = Language.objects.create(name="C#")

    def test_register_user(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivaylo',
            'last_name': 'Naidobriq',
            'faculty_number': '123',
            'known_technologies': '1',
            'password': '123'
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Competitor.objects.count(), 1)
        self.assertEqual(BaseUser.objects.count(), 1)

    def test_register_user_no_password(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivaylo',
            'last_name': 'Naidobriq',
            'faculty_number': '123',
            'known_technologies': '1',
        }
        url = reverse('hack_fmi:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    def setUp(self):
        self.language = Language.objects.create(name="C#")
        self.competitor = Competitor.objects.create(
            email='ivo@abv.bg',
            first_name='Ivaylo',
            last_name='Naidobriq',
            faculty_number='123',
        )
        self.competitor.set_password('123')
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
            first_name='Ivaylo',
            last_name='Naidobriq',
        )
        self.baseuser.set_password('123')
        self.baseuser.save()

        data = {
            'email': 'baseuser@abv.bg',
            'password': '123',
        }
        url = reverse('hack_fmi:login')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_two_times_same_token(self):
        data = {
            'email': 'ivo@abv.bg',
            'password': '123',
        }
        url = reverse('hack_fmi:login')
        response1 = self.client.post(url, data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.assertEqual(response1.data, response2.data)
