from test_plus.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from seed import factories
from base_app.models import GeneralPartner
from faker import Factory

faker = Factory.create()


class TestWebsite(TestCase):

    def setUp(self):
        self.client = Client()
        self.baseuser = factories.BaseUserFactory()
        self.student = factories.StudentFactory(
            baseuser_ptr_id=self.baseuser.id,
            email=self.baseuser.email)

    def test_index(self):
        url = reverse('website:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('HackBulgaria', str(response.content))

    def test_about(self):
        url = reverse('website:about')
        response = self.client.get(url)
        self.assertIn('snippets', str(response.context))

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
            course_id=course.id,
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
    # def test_course(self):
    #     url = reverse('website:course_detail')
    #     course = factories.CourseFactory()

    #     data = {
    #         'course_url': course.url
    #     }

    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, 200)

    # def test_forgotten_password_from_existing_user(self):
    #     url = reverse('website:forgotten_password')

    #     data = {
    #         'email': self.baseuser.email
    #     }

    #     import ipdb; ipdb.set_trace()  # breakpoint e2c6d81b //
    #     response = self.client.post(url, data)

    #     self.response_200(response)

    #     self.assertEqual(response.context['message'],
    #                     '''Email за промяна на паролата
    #                        беше изпратен на посочения адрес''')
