from django.test import TestCase
from django.core.urlresolvers import reverse
from post_office import mail

from post_office.models import EmailTemplate
from rest_framework import status
from rest_framework.test import APIClient
from base_app.models import Event, Ticket

from hack_fmi.models import BaseUser, Skill, Team
from .models import City
from hack_fmi.helper import date_decrease
from education.models import Course, CourseAssignment, Student, Certificate


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
        self.baseuser = BaseUser.objects.create_user(
            email="comp@comp.bg",
            password="123",
            full_name='Comp compov'
        )
        self.baseuser.is_active = True
        self.baseuser.make_competitor()
        self.baseuser.save()
        self.baseuser.is_vegetarian = True
        self.baseuser.needs_work = True
        self.skill = Skill.objects.create(name='C#')

        # make baseuser student
        self.student = Student(
            baseuser_ptr_id=self.baseuser.id,
        )

        self.student.save()
        self.student.__dict__.update(self.__dict__)
        self.student.save()

        self.course = Course.objects.create(
            name='Programming 101',
            application_until='2015-03-03',
            generate_certificates_until=date_decrease(1),
        )

        self.team = Team.objects.create(
            name='My Team',
        )
        self.ca = CourseAssignment.objects.create(
            course=self.course,
            user=self.student,
            group_time=1,
        )
        self.team.save()
        self.team.add_member(
            self.baseuser.get_competitor(), True
        )

        self.certificate = Certificate.objects.create(
            assignment=self.ca,
        )

        self.city = City.objects.create(
            name="Sofia"
        )
    def test_me_returns_full_team_membership_set(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.baseuser)
        url_me = reverse('base_app:me')
        response = self.client.get(url_me, format='json')
        resul_teammembership_set = response.data['competitor']['teammembership_set'][0]
        self.assertEqual(resul_teammembership_set['team']['name'], self.team.name)

    def test_me_returns_full_courseassignments_set(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.baseuser)
        url_me = reverse('base_app:me')
        response = self.client.get(url_me, format='json')
        # pp = pprint.PrettyPrinter(indent=2)
        # pp.pprint(response.data)
        first_courseassignment = response.data['student']['courseassignment_set'][0]
        self.assertEqual(first_courseassignment['course']['name'], self.course.name)

    def test_me_returns_certificate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.baseuser)
        url_me = reverse('base_app:me')
        response = self.client.get(url_me, format='json')
        certificate_id = response.data['student']['courseassignment_set'][0]['certificate']['id']
        self.assertEqual(certificate_id, self.certificate.id)

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


class EventTests(TestCase):

    def setUp(self):
        self.test_user = BaseUser.objects.create_user(
            email="comp@comp.bg",
            password="123",
            full_name='Comp compov'
        )
        self.event_conf = Event.objects.create(
            start_date="2012-01-01",
            end_date="2012-01-01",
            location="location text",
            description="Desc!",
            name='HackConf'
        )
        self.event_theater = Event.objects.create(
            start_date="2012-01-01",
            end_date="2012-01-01",
            location="location theater text",
            description="theater desc!",
            name='Theater!'
        )

    def test_get_all_events(self):
        count = Event.objects.count()
        url = reverse('base_app:event')
        response = self.client.get(url, format='json')
        self.assertEqual(count, len(response.data))

    def test_buy_ticket_for_event_not_logged(self):
        url = reverse('base_app:ticket')
        data = {'event': self.event_conf.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_buy_ticket_for_event_logged_user(self):
        count = Ticket.objects.count()
        self.client = APIClient()
        self.client.force_authenticate(user=self.test_user)
        url = reverse('base_app:ticket')
        data = {'event': self.event_conf.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        new_count = Ticket.objects.count()
        self.assertEqual(count+1, new_count)

    def test_buy_ticket_for_event_no_data(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.test_user)
        url = reverse('base_app:ticket')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)

# TODO: Find a nice way to do this!
    # def test_buy_two_tickets(self):
    #     self.client = APIClient()
    #     self.client.force_authenticate(user=self.test_user)
    #     url = reverse('base_app:ticket')
    #     data = {'event': self.event_conf.id}
    #     response = self.client.post(url, data)
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, 400)
