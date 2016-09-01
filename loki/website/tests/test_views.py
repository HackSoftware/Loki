from django.test import Client
from django.core.urlresolvers import reverse

from test_plus.test import TestCase
from post_office.models import EmailTemplate
from faker import Factory

from loki.seed import factories
from loki.base_app.models import GeneralPartner
from loki.base_app.models import BaseUser

faker = Factory.create()


class TestWebsite(TestCase):

    def setUp(self):
        self.client = Client()
        self.baseuser = factories.BaseUserFactory()
        self.student = factories.StudentFactory(
            baseuser_ptr_id=self.baseuser.id,
            email=self.baseuser.email)
        self.teacher = factories.TeacherFactory(
            baseuser_ptr_id=self.baseuser.id,
            email=self.baseuser.email
        )

    def test_index(self):
        url = reverse('website:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['snippets'])

    def test_about(self):
        url = reverse('website:about')
        response = self.client.get(url)

        self.assertIsNotNone(response.context['snippets'])

    def test_partners(self):
        company = factories.CompanyFactory()
        partner = factories.PartnerFactory(
            company=company
        )
        factories.GeneralPartnerFactory(
            partner=partner
        )

        url = reverse('website:partners')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(partner.company.logo)
        self.assertIn(partner.video_presentation, str(response.content))

        self.assertEquals(GeneralPartner.objects.count(), 1)

    def test_courses(self):
        url = reverse('website:courses')
        snippet1 = factories.SnippetFactory()

        course = factories.CourseFactory()
        courses = factories.CourseDescriptionFactory(
            course=course)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(courses.logo)
        self.assertIn(snippet1.label, response.context['snippets'])

    def test_login_from_active_user(self):

        url = reverse('website:login')
        self.baseuser.is_active = True
        self.baseuser.save()
        data = {
            'email': self.baseuser.email,
            'password': factories.BaseUserFactory.password
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('website:index'))

    def test_login_with_unvalid_data(self):
        url = reverse('website:login')
        data = {
            'email': self.baseuser.email,
            'password': factories.BaseUserFactory.password
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'],
                         'Невалидни email и/или парола')

    def test_login_wrong_pass(self):
        url = reverse('website:login')

        data = {
            'email': self.baseuser.email,
            'password': faker.password()
        }

        response = self.client.post(url, data)
        self.assertEqual(response.context['error'],
                         'Невалидни email и/или парола')
        self.assertEqual(response.status_code, 200)

    def test_login_user_not_active(self):
        url = reverse('website:login')
        self.baseuser.is_active = False
        self.baseuser.save()
        data = {
            'email': self.baseuser.email,
            'password': factories.BaseUserFactory.password
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['error'],
                         'Моля активирай акаунта си')

    def test_anonymous_required(self):
        self.baseuser.is_active = True
        self.baseuser.save()
        self.client.login(email=self.baseuser.email,
                          password=factories.BaseUserFactory.password)

        url = reverse('website:login')

        response = self.client.get(url)
        self.response_302(response)
        self.assertRedirects(response, reverse('website:profile'))

    def test_logout(self):
        self.baseuser.is_active = True
        self.baseuser.save()
        self.client.login(email=self.baseuser.email,
                          password=factories.BaseUserFactory.password)
        url = reverse('website:logout')
        self.client.login(email=self.baseuser.email,
                          password=factories.BaseUserFactory.password)

        response = self.client.get(url)

        self.response_302(response)
        self.assertRedirects(response, reverse('website:index'))

    def test_logout_login_required(self):
        url = reverse('website:logout')

        response = self.client.get(url)

        self.response_302(response)

    def test_profile(self):
        self.baseuser.is_active = True
        self.baseuser.save()
        self.client.login(email=self.baseuser.email,
                          password=factories.BaseUserFactory.password)

        url = reverse('website:profile')

        response = self.client.get(url)

        self.response_200(response)
        self.assertTemplateUsed(response, 'website/profile.html')

    def test_profile_login_required(self):
        url = reverse('website:profile')

        response = self.client.get(url)

        self.response_302(response)

    def test_profile_edit(self):
        self.baseuser.is_active = True
        self.baseuser.save()
        self.client.login(email=self.baseuser.email,
                          password=factories.BaseUserFactory.password)

        url = reverse('website:profile_edit')

        response = self.client.get(url)

        self.response_200(response)
        self.assertTemplateUsed(response, 'website/profile_edit.html')

    def test_course_detail_with_course_description(self):
        course = factories.CourseFactory()
        cd = factories.CourseDescriptionFactory(course=course)

        url = reverse('website:course_details',
                      kwargs={"course_url": cd.url})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/course_details.html')
        self.assertIsNotNone(response.context['snippets'])
        self.assertIsNotNone(response.context['course_days'])

    def test_register_get_query(self):
        url = reverse('website:register')

        get_resp = self.client.get(url)

        self.response_200(get_resp)
        self.assertIsNotNone(get_resp.context['form'])

    def test_register_if_not_registered(self):
        self.user_register = EmailTemplate.objects.create(
            name='user_register',
            subject='Регистриран потребител',
            content=faker.paragraph()
        )
        data = {
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'email': faker.email(),
            'password': 'sdfsdfd13',
        }
        url = reverse('website:register')

        post_resp = self.client.post(url, data)

        self.response_200(post_resp)

        made_user = BaseUser.objects.last()
        self.assertEqual(BaseUser.objects.filter(email=data['email']).count(),
                         1)
        self.assertEqual(made_user.email, data['email'])
        self.assertEqual(made_user.first_name,
                         data['first_name'])
        self.assertEqual(made_user.last_name, data['last_name'])
        self.assertTrue(made_user.check_password(data['password']))
        self.assertTemplateUsed(post_resp, 'website/auth/thanks.html')

    def test_register_anonymous_required(self):
        self.baseuser.is_active = True
        self.baseuser.save()
        self.client.login(email=self.baseuser.email,
                          password=factories.BaseUserFactory.password)

        url = reverse('website:register')

        post_resp = self.client.get(url)

        self.response_302(post_resp)

    def test_forgotten_password_from_existing_user(self):
        self.pass_reset = EmailTemplate.objects.create(
            name='password_reset',
            subject='Смяна на парола',
            content=faker.paragraph()
        )

        url = reverse('website:forgotten_password')

        data = {
            'email': self.baseuser.email
        }

        response = self.client.post(url, data)

        self.response_200(response)

        self.assertEqual(response.context['message'],
                         'Email за промяна на паролата беше изпратен на посочения адрес')

    def test_forgotten_password_from_non_existing_user(self):
        self.pass_reset = EmailTemplate.objects.create(
            name='password_reset',
            subject='Смяна на парола',
            content=faker.paragraph()
        )

        url = reverse('website:forgotten_password')

        data = {
            'email': faker.email()
        }

        response = self.client.post(url, data)

        self.response_200(response)

        self.assertEqual(response.context['message'],
                         'Потребител с посочения email не е открит')
