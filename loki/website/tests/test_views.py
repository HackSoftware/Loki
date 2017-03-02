from django.test import Client
from django.core.urlresolvers import reverse
from django.core import mail

from test_plus.test import TestCase
from faker import Factory

from loki.seed import factories
from loki.base_app.models import GeneralPartner
from loki.base_app.models import BaseUser
from loki.education.models import Student, CheckIn, Teacher, WorkingAt

faker = Factory.create()


class TestWebsite(TestCase):

    def setUp(self):
        self.client = Client()
        self.baseuser = factories.BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()

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
        factories.CourseDescriptionFactory(course=course)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(snippet1.label, response.context['snippets'])

    def test_login_from_active_user(self):

        url = reverse('website:login')
        data = {
            'email': self.baseuser.email,
            'password': factories.BaseUserFactory.password
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('website:profile'))

    def test_login_with_unvalid_data(self):
        url = reverse('website:login')
        data = {
            'email': faker.email(),
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
        self.client.login(email=self.baseuser.email,
                          password=factories.BaseUserFactory.password)

        url = reverse('website:login')

        response = self.client.get(url)
        self.response_302(response)
        self.assertRedirects(response, reverse('website:profile'))

    def test_logout(self):
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
        self.assertEqual(len(mail.outbox), 1)

    def test_register_anonymous_required(self):
        self.client.login(email=self.baseuser.email,
                          password=factories.BaseUserFactory.password)

        url = reverse('website:register')

        post_resp = self.client.get(url)

        self.response_302(post_resp)

    from django.test import override_settings

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_forgotten_password_from_existing_user(self):
        url = reverse('website:forgotten_password')

        data = {
            'email': self.baseuser.email
        }

        response = self.client.post(url, data)

        self.response_200(response)

        self.assertEqual(response.context['message'],
                         'Email за промяна на паролата беше изпратен на посочения адрес')
        self.assertEqual(len(mail.outbox), 1)

    def test_forgotten_password_from_non_existing_user(self):
        url = reverse('website:forgotten_password')

        data = {
            'email': faker.email()
        }

        response = self.client.post(url, data)

        self.response_200(response)

        self.assertEqual(response.context['message'],
                         'Потребител с посочения email не е открит')
        self.assertEqual(len(mail.outbox), 0)

    def test_edit_student_profile(self):
        student = BaseUser.objects.promote_to_student(self.baseuser)
        with self.login(email=student.email,
                        password=factories.BaseUserFactory.password):
            data = {'mac': "a1:b2:c3:d4:e5:00"}
            response = self.post('website:profile_edit_student', data=data, follow=True)
            self.response_200(response)

        self.assertEqual(data['mac'], Student.objects.get(email=student.email).mac)

    def test_check_ins_for_edit_student_profile(self):
        check_in = factories.CheckInFactory(user=None)
        mac = check_in.mac
        student = BaseUser.objects.promote_to_student(self.baseuser)

        with self.login(email=student.email,
                        password=factories.BaseUserFactory.password):

            data = {'mac': mac}
            response = self.post('website:profile_edit_student', data=data, follow=True)
            self.response_200(response)

        self.assertEqual(mac, Student.objects.get(email=student.email).mac)
        self.assertEqual(student.baseuser_ptr_id,
                         CheckIn.objects.filter(mac__iexact=mac).first().user.id)

    def test_check_ins_for_edit_teacher_profile(self):
        check_in = factories.CheckInFactory(user=None)
        mac = check_in.mac

        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        with self.login(email=teacher.email,
                        password=factories.BaseUserFactory.password):

            data = {'mac': mac}
            response = self.post('website:profile_edit_teacher', data=data, follow=True)
            self.response_200(response)

        self.assertEqual(mac, Teacher.objects.get(email=teacher.email).mac)
        self.assertEqual(teacher.baseuser_ptr_id,
                         CheckIn.objects.filter(mac__iexact=mac).first().user.id)


class WorkingAtTests(TestCase):

    def setUp(self):
        self.baseuser = factories.BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()

    def test_unsigned_user_cannot_access_workingat_form(self):
        response = self.get('website:working-at')
        self.assertEquals(response.status_code, 302)

    def test_baseuser_cannot_access_workingat_form(self):
        student = BaseUser.objects.promote_to_student(self.baseuser)
        self.assertEquals(isinstance(student.get_student(), Student), True)
        with self.login(username=student.email, password=factories.BaseUserFactory.password):
            response = self.get('website:working-at')
            self.assertEquals(response.status_code, 200)

    def test_student_can_access_workingat_form(self):
        with self.login(username=self.baseuser.email, password=factories.BaseUserFactory.password):
            response = self.get('website:working-at')
            self.assertEquals(response.status_code, 404)

    def test_teacher_cannot_access_workingat_form(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        self.assertEquals(teacher.get_student(), False)
        with self.login(username=teacher.email, password=factories.BaseUserFactory.password):
            response = self.get('website:working-at')
            self.assertEquals(response.status_code, 404)

    def test_teacher_who_is_student_access_workingat_form(self):
        teacher_student = BaseUser.objects.promote_to_teacher(self.baseuser)
        BaseUser.objects.promote_to_student(self.baseuser)
        self.assertEquals(isinstance(teacher_student.get_teacher(), Teacher), True)
        self.assertEquals(isinstance(teacher_student.get_student(), Student), True)
        with self.login(username=teacher_student.email, password=factories.BaseUserFactory.password):
            response = self.get('website:working-at')
            self.assertEquals(response.status_code, 200)

    def test_student_fill_working_at_form_with_existing_company(self):
        student = BaseUser.objects.promote_to_student(self.baseuser)
        company = factories.CompanyFactory()
        self.assertEquals(WorkingAt.objects.filter(student=student).count(), 0)
        with self.login(username=student.email, password=factories.BaseUserFactory.password):
            data = {
                'company': company.id,
                'start_date': faker.date(),
                'title': faker.text(max_nb_chars=50)
            }
            response = self.post('website:working-at', data=data)
            self.assertEquals(WorkingAt.objects.filter(student=student).count(), 1)
            self.assertEquals(response.status_code, 302)
            self.assertRedirects(response, reverse('website:profile'))

    def test_student_fill_working_at_form_with_nonexisting_company(self):
        student = BaseUser.objects.promote_to_student(self.baseuser)
        factories.CompanyFactory()
        self.assertEquals(WorkingAt.objects.filter(student=student).count(), 0)
        with self.login(username=student.email, password=factories.BaseUserFactory.password):
            data = {
                'company': faker.text(max_nb_chars=20),
                'start_date': faker.date(),
                'title': faker.text(max_nb_chars=50)
            }
            response = self.post('website:working-at', data=data)
            working_at = WorkingAt.objects.filter(student=student)
            self.assertEquals(working_at.count(), 1)
            self.assertIsNone(working_at.last().company)
            self.assertEqual(working_at.last().company_name, data['company'])
            self.assertEquals(response.status_code, 302)
            self.assertRedirects(response, reverse('website:profile'))

    def test_student_looking_for_job(self):
        student = BaseUser.objects.promote_to_student(self.baseuser)
        # default value is False, we are going to set it to True
        updated_looking_for_job = True
        with self.login(username=student.email, password=factories.BaseUserFactory.password):
            data = {
                'looking_for_job': updated_looking_for_job
            }
            response = self.post('website:update_looking_for_job', data=data)
            self.assertEquals(Student.objects.get(id=student.id).looking_for_job,
                              data['looking_for_job'])
            self.assertEquals(response.status_code, 302)
            self.assertRedirects(response, reverse('website:profile'))

    def test_profile_data_after_creating_workingat_objects(self):
        student = BaseUser.objects.promote_to_student(self.baseuser)
        self.assertEquals(WorkingAt.objects.filter(student=student).count(), 0)
        job = factories.WorkingAtFactory(student=student)
        self.assertEquals(WorkingAt.objects.filter(student=student).count(), 1)
        with self.login(username=student.email, password=factories.BaseUserFactory.password):
            response = self.get('website:profile')
            self.assertEquals(response.status_code, 200)
            self.assertIn(job, response.context['jobs'])
