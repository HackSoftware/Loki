from django.test import TestCase
from django.core.urlresolvers import reverse
from post_office import mail

from post_office.models import EmailTemplate
from rest_framework import status
from rest_framework.test import APIClient

from hack_fmi.models import BaseUser, Skill


class BaseUserRegistrationTests(TestCase):

    def setUp(self):
        self.user_register = EmailTemplate.objects.create(
            name='user_register',
            subject='Регистриран потребител',
            content='Lorem ipsum dolor sit amet, consectetur adipisicing'
        )

    def test_register_base_user(self):
        user_mail = 'sten@gmail.com'
        data = {
            'email': user_mail,
            'first_name': 'Stanislav',
            'last_name': 'Bozhanov',
            'password': '123',
        }
        url = reverse('base_app:register')
        count = BaseUser.objects.count()
        self.client.post(url, data, format='json')
        self.assertEqual(count + 1, BaseUser.objects.count())

    def test_register_user_no_password(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': 'Bachvarov',
        }
        url = reverse('base_app:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_sent(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': ' Bachvarov',
            'password': '123',
        }
        url = reverse('base_app:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.get_queued()), 1)

    def test_email_sent_new_template(self):
        data = {
            'email': 'ivo@abv.bg',
            'first_name': 'Ivo',
            'last_name': ' Bachvarov',
            'password': '123'
        }
        url = reverse('base_app:register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.user_register.content, mail.get_queued()[0].message)


class PersonalUserInformationTests(TestCase):
    def setUp(self):
        self.competitor = BaseUser.objects.create_user(
            email="comp@comp.bg",
            password="123",
            full_name='Comp compov'
        )
        self.competitor.is_active = True
        self.competitor.make_competitor()
        self.competitor.save()
        self.competitor.is_vegetarian = True
        self.competitor.needs_work = True
        self.skill = Skill.objects.create(name='C#')

    def test_me_returns_all_info(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.competitor)
        url_me = reverse('base_app:me')
        response = self.client.get(url_me, format='json')
        print(response.data)
