import os

from test_plus.test import TestCase

from faker import Factory
from datetime import datetime

from loki.seed import factories
from loki.base_app.models import RegisterOrigin
from loki.base_app.helper import get_activation_url
from loki.website.forms import RegisterForm

faker = Factory.create()


class BaseUserRegistrationTests(TestCase):

    def setUp(self):

        self.city1 = factories.CityFactory()
        self.user = factories.BaseUserFactory(birth_place=self.city1)
        self.education_place = factories.EducationPlaceFactory(city=self.city1)
        self.university = factories.UniversityFactory()
        self.faculty = factories.FacultyFactory(university=self.university)
        self.subject = factories.SubjectFactory(faculty=self.faculty)
        factories.\
            EducationInfoFactory(user=self.user,
                                 place=self.education_place,
                                 faculty=self.faculty,
                                 subject=self.subject)

        self.academy = factories.AcademyFactory()

        self.user_data = {
            'email': faker.email(),
            'first_name': faker.text(max_nb_chars=20),
            'last_name': faker.text(max_nb_chars=20),
            'password': faker.password(),
            'g-recaptcha-response': 'PASSED'
        }
        self.user_reg_form = {
            'studies_at': faker.country(),
            'start_date': faker.date(pattern="%d-%m-%Y"),
            'end_date': faker.date(pattern="%d-%m-%Y")
        }
        self.user_reg_form.update(self.user_data)

        self.reg_form_with_faculty_ed_place = {
            'faculty': self.faculty.id,
            'educationplace': self.education_place.id
        }
        self.reg_form_with_faculty_ed_place.update(self.user_reg_form)

        self.reg_form_with_academy = {
            'educationplace': self.academy.id
        }
        self.reg_form_with_academy.update(self.user_reg_form)
        # add recaptcha testing env on Register
        os.environ['RECAPTCHA_TESTING'] = 'True'

    def tearDown(self):
        del os.environ['RECAPTCHA_TESTING']

    def test_register_base_user_via_form(self):
        reg_form = RegisterForm(data=self.user_reg_form)

        self.assertTrue(reg_form.is_valid())
        user = reg_form.save()
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.email, self.user_data['email'])
        self.\
            assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.created_at.date(), datetime.now().date())

    def test_get_activation_url(self):
        RegisterOrigin.objects.create(
            name='hackfmi',
            redirect_url='http://ragister.hackfmi.com/#/login')

        url_with_origin = get_activation_url('token', 'hackfmi')
        url_without_origin = get_activation_url('token')

        self.assertTrue('?origin=' in url_with_origin)
        self.assertFalse('?origin=' in url_without_origin)
