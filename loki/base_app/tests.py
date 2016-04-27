from datetime import date
from django.test import TestCase
from django.core.urlresolvers import reverse
from post_office import mail

from post_office.models import EmailTemplate
from rest_framework import status
from rest_framework.test import APIClient

from hack_fmi.models import Skill, Team
from .models import BaseUser, City, EducationInfo, School, Academy, University, Faculty, Subject
from .helper import get_activation_url
from hack_fmi.helper import date_decrease
from education.models import Course, CourseAssignment, Student, Certificate
from website.forms import RegisterForm

import unittest


class BaseUserRegistrationTests(TestCase):

    def setUp(self):
        self.user_register = EmailTemplate.objects.create(
            name='user_register',
            subject='Регистриран потребител',
            content='Lorem ipsum dolor sit amet, consectetur adipisicing'
        )

        self.base_user_base_info = {
            "first_name": "Robert",
            "last_name": "Paulson",
            "email": "zombie@underworld.dead",
            "password": "1want3omebrain3",
            "studies_at": "",
            "educationplace": None,
            "faculty": None,
            "subject": None
        }

        self.city1 = City.objects.create(name='Monstropolis')
        self.city2 = City.objects.create(name='Death City')

        self.university = University.objects.create(city=self.city1, name="Monsters University")
        self.faculty = Faculty.objects.create(university=self.university, name="School of Scaring")
        self.subject = Subject.objects.create(faculty=self.faculty, name="SCAR101.Intro to Scaring")

        self.academy = Academy.objects.create(city=self.city2, name="Shibusen")

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

    def test_register_base_user_via_form(self):
        user_info = self.base_user_base_info
        user_info['studies_at'] = "underworld"
        user_info['start_date'] = date(2000, 10, 1)
        user_info['end_date'] = date(2005, 10, 1)

        reg_form = RegisterForm(user_info)

        self.assertTrue(reg_form.is_valid())
        user = reg_form.save()
        self.assertEqual(user.first_name, "Robert")
        self.assertEqual(user.last_name, "Paulson")
        self.assertEqual(user.email, "zombie@underworld.dead")
        self.assertTrue(user.check_password("1want3omebrain3"))

    def test_register_base_user_via_form_with_ed_place(self):
        user_info = self.base_user_base_info
        user_info["educationplace"] = self.university.id
        user_info["faculty"] = self.faculty.id
        user_info["subject"] = self.subject.id
        user_info['start_date'] = date(2000, 10, 1)
        user_info['end_date'] = date(2005, 10, 1)

        reg_form = RegisterForm(user_info)

        self.assertTrue(reg_form.is_valid())
        user = reg_form.save()

        self.assertEqual(user.first_name, "Robert")
        self.assertEqual(user.last_name, "Paulson")
        self.assertEqual(user.email, "zombie@underworld.dead")
        self.assertTrue(user.check_password, "1want3omebrain3")

        self.assertEqual(len(user.educationinfo_set.all()), 1)
        self.assertEqual(user.educationinfo_set.first().place.name, self.university.name)
        self.assertEqual(user.educationinfo_set.first().place.city.name, self.city1.name)
        self.assertEqual(user.educationinfo_set.first().faculty.name, self.faculty.name)
        self.assertEqual(user.educationinfo_set.first().subject.name, self.subject.name)
        self.assertIsNone(user.studies_at)

    def test_register_base_user_via_form_with_studies_at(self):
        user_info = self.base_user_base_info
        user_info['studies_at'] = "Home"
        user_info['start_date'] = date(2000, 10, 1)
        user_info['end_date'] = date(2005, 10, 1)

        reg_form = RegisterForm(user_info)

        self.assertTrue(reg_form.is_valid())
        user = reg_form.save()

        self.assertEqual(user.first_name, "Robert")
        self.assertEqual(user.last_name, "Paulson")
        self.assertEqual(user.email, "zombie@underworld.dead")
        self.assertTrue(user.check_password, "1want3omebrain3")

        self.assertEqual(len(user.educationinfo_set.all()), 0)
        self.assertEqual(user.studies_at, "Home")

    def test_register_base_user_via_form_with_academy(self):
        user_info = self.base_user_base_info
        user_info["educationplace"] = self.academy.id
        user_info['start_date'] = date(2000, 10, 1)
        user_info['end_date'] = date(2005, 10, 1)

        reg_form = RegisterForm(user_info)

        self.assertTrue(reg_form.is_valid())
        user = reg_form.save()

        self.assertEqual(user.first_name, "Robert")
        self.assertEqual(user.last_name, "Paulson")
        self.assertEqual(user.email, "zombie@underworld.dead")
        self.assertTrue(user.check_password, "1want3omebrain3")

        self.assertEqual(len(user.educationinfo_set.all()), 1)
        self.assertEqual(user.educationinfo_set.first().place.name, self.academy.name)
        self.assertEqual(user.educationinfo_set.first().place.city.name, self.city2.name)
        self.assertIsNone(user.educationinfo_set.first().faculty)
        self.assertIsNone(user.educationinfo_set.first().subject)
        self.assertIsNone(user.studies_at)

    def test_get_activation_url(self):
        url_with_origin = get_activation_url('token', 'register.hackfmi.com')
        url_without_origin = get_activation_url('token')

        self.assertTrue('?origin=' in url_with_origin)
        self.assertFalse('?origin=' in url_without_origin)

# class PersonalUserInformationTests(TestCase):

#     def setUp(self):
#         self.baseuser = BaseUser.objects.create_user(
#             email="comp@comp.bg",
#             password="123",
#             full_name='Comp compov'
#         )
#         self.baseuser.is_active = True
#         # self.baseuser.make_competitor()
#         self.baseuser.save()
#         self.baseuser.is_vegetarian = True
#         self.baseuser.needs_work = True
#         self.skill = Skill.objects.create(name='C#')

#         # make baseuser student
#         self.student = Student(
#             baseuser_ptr_id=self.baseuser.id,
#         )

#         self.student.save()
#         self.student.__dict__.update(self.__dict__)
#         self.student.save()

#         self.course = Course.objects.create(
#             name='Programming 101',
#             application_until='2015-03-03',
#             generate_certificates_until=date_decrease(1),
#         )

#         self.team = Team.objects.create(
#             name='My Team',
#         )
#         self.ca = CourseAssignment.objects.create(
#             course=self.course,
#             user=self.student,
#             group_time=1,
#         )
#         self.team.save()
#         self.team.add_member(
#             self.baseuser.get_competitor(), True
#         )

#         self.certificate = Certificate.objects.create(
#             assignment=self.ca,
#         )

#         self.city = City.objects.create(
#             name="Sofia"
#         )

#     def test_me_returns_full_team_membership_set(self):
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.baseuser)
#         url_me = reverse('base_app:me')
#         response = self.client.get(url_me, format='json')
#         resul_teammembership_set = response.data['competitor']['teammembership_set'][0]
#         self.assertEqual(resul_teammembership_set['team']['name'], self.team.name)

#     def test_me_returns_full_courseassignments_set(self):
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.baseuser)
#         url_me = reverse('base_app:me')
#         response = self.client.get(url_me, format='json')
#         # pp = pprint.PrettyPrinter(indent=2)
#         # pp.pprint(response.data)
#         first_courseassignment = response.data['student']['courseassignment_set'][0]
#         self.assertEqual(first_courseassignment['course']['name'], self.course.name)

#     def test_me_returns_certificate(self):
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.baseuser)
#         url_me = reverse('base_app:me')
#         response = self.client.get(url_me, format='json')
#         certificate_token = response.data['student']['courseassignment_set'][0]['certificate']['token']
#         self.assertEqual(certificate_token, str(self.certificate.token))

#     def test_baseuser_update(self):
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.baseuser)
#         update_url = reverse('base_app:update_baseuser')
#         data = {'github_account': 'http://github.com/Ivo'}
#         response = self.client.patch(update_url, data, format='json')
#         baseuser = BaseUser.objects.get(id=self.baseuser.id)

#         self.assertEqual(baseuser.github_account, data['github_account'])

#     def test_patch_empty_birth_place(self):
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.baseuser)
#         update_url = reverse('base_app:update_baseuser')
#         data = {'birth_place': self.city.id}

#         self.client.patch(update_url, data, format='json')
#         baseuser = BaseUser.objects.get(id=self.baseuser.id)
#         self.assertEqual(baseuser.birth_place, self.city)
