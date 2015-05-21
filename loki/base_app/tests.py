from django.test import TestCase
from django.core.urlresolvers import reverse

from post_office.models import EmailTemplate

from hack_fmi.models import BaseUser


class BaseUserTests(TestCase):

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
        url = reverse('base:register')
        count = BaseUser.objects.count()
        self.client.post(url, data, format='json')
        self.assertEqual(count + 1, BaseUser.objects.count())
