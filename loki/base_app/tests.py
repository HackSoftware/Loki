from django.test import TestCase
from django.core.urlresolvers import reverse
from post_office import mail

from post_office.models import EmailTemplate
from rest_framework import status
from .models import BaseUser, RegisterOrigin
from .helper import get_activation_url
from website.forms import RegisterForm
from rest_framework.test import APIClient

from faker import Factory
from seed import factories

import unittest

from datetime import date

from hack_fmi.models import Skill, Team
from .helper import get_activation_url
from hack_fmi.helper import date_decrease
from education.models import Course, CourseAssignment, Student, Certificate
from website.forms import RegisterForm


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

        self.user_register = EmailTemplate.objects.create(
            name='user_register',
            subject='Регистриран потребител',
            content='Lorem ipsum dolor sit amet, consectetur adipisicing'
        )
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
            # 'faculty': self.faculty.id,
            'educationplace': self.academy.id
        }
        self.reg_form_with_academy.update(self.user_reg_form)

    def test_register_base_user(self):
        url = reverse('base_app:register')
        count = BaseUser.objects.count()
        self.client.post(url, self.user_data, format='json')
        self.assertEqual(count + 1, BaseUser.objects.all().count())

    def test_register_user_no_password(self):
        self.user_data_without_pass = {
            k: v for k, v in self.user_data.items() if k != 'password'}

        url = reverse('base_app:register')
        response = self.client.post(url,
                                    self.user_data_without_pass, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_sent(self):
        url = reverse('base_app:register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.get_queued()), 1)

    def test_email_sent_new_template(self):
        url = reverse('base_app:register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(self.user_register.content, mail.get_queued()[0].message)

    def test_register_base_user_via_form(self):
        reg_form = RegisterForm(data=self.user_reg_form)

        self.assertTrue(reg_form.is_valid())
        user = reg_form.save()
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.email, self.user_data['email'])
        self.\
            assertTrue(user.check_password(self.user_data['password']))

    def test_register_base_user_via_form_with_ed_place_and_faculty(self):
        reg_form = RegisterForm(self.reg_form_with_faculty_ed_place)

        self.assertTrue(reg_form.is_valid())
        user = reg_form.save()

        self.assertEqual(user.first_name,
                         self.reg_form_with_faculty_ed_place['first_name'])
        self.assertEqual(user.last_name,
                         self.reg_form_with_faculty_ed_place['last_name'])
        self.assertEqual(user.email,
                         self.reg_form_with_faculty_ed_place['email'])
        self.assertTrue(user.check_password,
                        self.reg_form_with_faculty_ed_place['password'])

        self.assertEqual(self.user.education_info.count(), 1)
        self.assertEqual(self.user.education_info.first().name,
                         self.university.name)
        self.assertEqual(self.user.education_info.first().city.name,
                         self.city1.name)
        self.assertEqual(self.faculty.related_fac_to_user.first().user,
                         self.user)
        self.assertEqual(self.subject.related_subj_to_user.first().user,
                         self.user)

    def test_register_base_user_via_form_with_academy(self):
        reg_form = RegisterForm(self.reg_form_with_academy)

        self.assertTrue(reg_form.is_valid())
        user = reg_form.save()

        self.assertEqual(user.first_name,
                         self.reg_form_with_faculty_ed_place['first_name'])
        self.assertEqual(user.last_name,
                         self.reg_form_with_faculty_ed_place['last_name'])
        self.assertEqual(user.email,
                         self.reg_form_with_faculty_ed_place['email'])
        self.assertTrue(user.check_password,
                        self.reg_form_with_faculty_ed_place['password'])

        self.assertEqual(self.user.education_info.count(), 1)
        self.assertEqual(self.user.education_info.first().name,
                         self.academy.name)
        self.assertEqual(self.user.education_info.first().city.name,
                         self.city1.name)

    def test_get_activation_url(self):
        RegisterOrigin.objects.create(
            name='hackfmi',
            redirect_url='http://ragister.hackfmi.com/#/login')

        url_with_origin = get_activation_url('token', 'hackfmi')
        url_without_origin = get_activation_url('token')

        self.assertTrue('?origin=' in url_with_origin)
        self.assertFalse('?origin=' in url_without_origin)

    def test_login(self):
        reg_url = reverse('base_app:register')
        self.client.post(reg_url, self.user_data, format='json')

        login_url = reverse('base_app:login')
        self.client.post(login_url, self.user_data, format='json')


class PersonalUserInformationTests(TestCase):

    def setUp(self):
        self.company = factories.CompanyFactory()
        self.partner = factories.PartnerFactory(company=self.company)
        self.course = factories.CourseFactory()
        self.baseuser = factories.BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.is_vegeterian = True
        self.baseuser.needs_work = True

        # make baseuser student
        self.student = factories.StudentFactory(
            baseuser_ptr_id=self.baseuser.id,
        )

        self.student.__dict__.update(self.__dict__)

        self.skill = factories.SkillFactory()
        self.season = factories.SeasonFactory()
        self.room = factories.RoomFactory(season=self.season)
        self.fmi_partner = factories.HackFmiPartnerFactory()
        self.fmi_partner2 = factories.HackFmiPartnerFactory()
        self.mentor = factories.MentorFactory(from_company=self.fmi_partner)
        self.team = factories.TeamFactory()
        self.courseAssignmet = factories.\
            CourseAssignmentFactory(course=self.course,
                                    user=self.student)
        self.courseAssignmet.favourite_partners.add(self.partner)
        self.competitor = factories.CompetitorFactory(
            baseuser_ptr_id=self.baseuser.id,)
        self.team.add_member(competitor=self.competitor)

        # cert = factories.CertificateFactory(assignment_id=self.courseAssignmet.id)
        self.city = factories.CityFactory()

    def test_me_returns_full_team_membership_set(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.baseuser)
        url_me = reverse('base_app:me')
        response = self.client.get(url_me, format='json')
        resul_teammembership_set = response.\
            data['competitor']['teammembership_set'][0]
        self.assertEqual(resul_teammembership_set['team']['name'],
                         self.team.name)

    def test_me_returns_full_courseassignments_set(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.baseuser)
        url_me = reverse('base_app:me')
        response = self.client.get(url_me, format='json')
        # pp = pprint.PrettyPrinter(indent=2)
        # pp.pprint(response.data)
        first_courseassignment = response.\
            data['student']['courseassignment_set'][0]
        self.assertEqual(first_courseassignment['course']['name'],
                         self.course.name)

    # def test_me_returns_certificate(self):
    #     self.client = APIClient()
    #     self.client.force_authenticate(user=self.baseuser)
    #     url_me = reverse('base_app:me')
    #     response = self.client.get(url_me, format='json')
    #     certificate_token = response.\
    #         data['student']['courseassignment_set'][0]['certificate']['token']
    #     self.assertEqual(certificate_token, str(self.certificate.token))

    def test_baseuser_update(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.baseuser)
        update_url = reverse('base_app:update_baseuser')
        data = {'github_account': 'http://github.com/Ivo'}
        response = self.client.patch(update_url, data, format='json')
        baseuser = BaseUser.objects.get(id=self.baseuser.id)

        self.assertEqual(baseuser.github_account, data['github_account'])

    def test_patch_empty_birth_place(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.baseuser)
        update_url = reverse('base_app:update_baseuser')
        data = {'birth_place': self.city.id}

        self.client.patch(update_url, data, format='json')
        baseuser = BaseUser.objects.get(id=self.baseuser.id)
        self.assertEqual(baseuser.birth_place, self.city)
