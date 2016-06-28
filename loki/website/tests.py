from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from seed import factories
from base_app.models import GeneralPartner
from faker import Factory

faker = Factory.create()


class TestWebsite(TestCase):

    def SetUp(self):
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

        # import pytest;pytest.set_trace()

    
    # def test_course(self):
    #     url = reverse('website:course_detail')
    #     course = factories.CourseFactory()

    #     data = {
    #         'course_url': course.url
    #     }

    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, 200)


