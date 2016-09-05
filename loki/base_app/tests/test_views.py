from django.core.urlresolvers import reverse
from django.core import mail

from test_plus.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from faker import Factory

from loki.seed import factories
from loki.base_app.models import BaseUser, RegisterOrigin
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
            'password': faker.password()
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

    def test_register_base_user_via_form(self):
        reg_form = RegisterForm(data=self.user_reg_form)

        self.assertTrue(reg_form.is_valid())
        user = reg_form.save()
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.email, self.user_data['email'])
        self.\
            assertTrue(user.check_password(self.user_data['password']))

    def test_get_activation_url(self):
        RegisterOrigin.objects.create(
            name='hackfmi',
            redirect_url='http://ragister.hackfmi.com/#/login')

        url_with_origin = get_activation_url('token', 'hackfmi')
        url_without_origin = get_activation_url('token')

        self.assertTrue('?origin=' in url_with_origin)
        self.assertFalse('?origin=' in url_without_origin)


class PersonalUserInformationTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.company = factories.CompanyFactory()
        self.partner = factories.PartnerFactory(company=self.company)
        self.course = factories.CourseFactory()
        self.baseuser = factories.BaseUserFactory()
        self.baseuser.is_active = True

        self.student = factories.StudentFactory(
            baseuser_ptr_id=self.baseuser.id,
            email=self.baseuser.email
        )

        self.student.__dict__.update(self.__dict__)

        self.team = factories.TeamFactory()
        self.courseAssignment = factories.\
            CourseAssignmentFactory(course=self.course,
                                    user=self.student)
        self.courseAssignment.favourite_partners.add(self.partner)
        self.competitor = factories.CompetitorFactory(
            baseuser_ptr_id=self.baseuser.id,)
        self.team.add_member(competitor=self.competitor)

        self.certificate = factories.CertificateFactory(
            assignment_id=self.courseAssignment.id,
            assignment=self.courseAssignment)

        self.city = factories.CityFactory()

    def test_me_returns_full_team_membership_set(self):
        self.client.force_authenticate(user=self.baseuser)
        url_me = reverse('base_app:me')
        response = self.client.get(url_me, format='json')
        resul_teammembership_set = response.\
            data['competitor']['teammembership_set'][0]

        self.assertEqual(resul_teammembership_set['team'],
                         self.team.id)

    def test_me_returns_full_courseassignments_set(self):
        self.client.force_authenticate(user=self.baseuser)
        url_me = reverse('base_app:me')
        response = self.client.get(url_me, format='json')
        first_courseassignment = response.\
            data['student']['courseassignment_set'][0]
        self.assertEqual(first_courseassignment['course']['name'],
                         self.course.name)

    def test_me_returns_certificate(self):
        self.client.force_authenticate(user=self.baseuser)
        url_me = reverse('base_app:me')
        response = self.client.get(url_me, format='json')
        certificate_token = response.\
            data['student']['courseassignment_set'][0]['certificate']['token']
        self.assertEqual(certificate_token, str(self.certificate.token))

    def test_baseuser_update(self):
        self.client.force_authenticate(user=self.baseuser)
        update_url = reverse('base_app:update_baseuser')
        data = {'github_account': 'http://github.com/Ivo'}
        self.client.patch(update_url, data, format='json')
        baseuser = BaseUser.objects.get(id=self.baseuser.id)

        self.assertEqual(baseuser.github_account, data['github_account'])

    def test_update_empty_birth_place(self):
        self.client.force_authenticate(user=self.baseuser)
        update_url = reverse('base_app:update_baseuser')
        data = {'birth_place': self.city.id}

        self.client.patch(update_url, data)
        baseuser = BaseUser.objects.get(id=self.baseuser.id)
        self.assertEqual(baseuser.birth_place, self.city)

    def test_try_to_update_user_info_if_not_authenticated(self):
        update_url = reverse('base_app:update_baseuser')
        data = {'birth_place': self.city.id}

        response = self.client.patch(update_url, data)
        self.response_401(response)
