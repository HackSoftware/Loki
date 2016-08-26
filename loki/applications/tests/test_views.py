from datetime import timedelta

from django.utils import timezone

from test_plus.test import TestCase

from seed.factories import CourseFactory
from ..models import ApplicationInfo
from seed.factories import (faker,
                            CourseFactory, BaseUserFactory, CourseDescriptionFactory,
                            ApplicationInfoFactory, ApplicationProblemFactory,
                            ApplicationProblemSolutionFactory, ApplicationFactory)
from ..models import Application, ApplicationProblem, ApplicationProblemSolution
from ..views import apply_course

class TestApplicationViews(TestCase):
    def setUp(self):
        self.course = CourseFactory()
        self.user = BaseUserFactory()
        self.user.is_active = True
        self.user.save()
        self.course_description = CourseDescriptionFactory(course=self.course)
        self.application_info = ApplicationInfoFactory(course=self.course)
        # self.application = ApplicationFactory(application_info=self.application_info,
                                            #   user=self.user)

    def test_non_registered_user_cannot_see_apply_overview(self):
        self.get('website:apply_overview')
        self.response_302()

    def test_registered_user_can_see_apply_overview(self):
        with self.login(username=self.user.email, password=BaseUserFactory.password):
            self.get('website:apply_overview')
            self.response_200()

    def test_applying_for_non_existing_course_should_raise_404(self):
        self.assertEqual(0, Application.objects.count())

        with self.login(username=self.user.email, password=BaseUserFactory.password):
            data = {}
            self.post('website:apply_course',
                      course_url=self.course_description.url + faker.word(),
                      data=data)
            self.response_404()

        self.assertEqual(0, Application.objects.count())

    def test_register_user_can_see_course_apply_form(self):
        with self.login(username=self.user.email, password=BaseUserFactory.password):
            self.get('website:apply_course', course_url=self.course_description.url)
            self.response_200()

    def test_applying_for_course_with_inconsistent_data(self):
        self.assertEqual(0, Application.objects.count())

        with self.login(username=self.user.email, password=BaseUserFactory.password):
            data = {"phone": faker.random_number(),
                    "skype": faker.word()}
            response = self.post('website:apply_course',
                      course_url=self.course_description.url,
                      data=data)
            form = self.get_context('form')
            errors = {'studies_at': ['Това поле е задължително.'],
                      'works_at': ['Това поле е задължително.'],
                      'task_field_count': ['Това поле е задължително.']}
            self.assertEquals(errors, form.errors)
            self.response_200()

        self.assertEqual(0, Application.objects.count())


    def test_applying_for_course(self):
        self.assertEqual(0, Application.objects.count())
        app_problem1 = ApplicationProblemFactory()
        app_problem2 = ApplicationProblemFactory()
        self.application_info.applicationproblem_set.add(app_problem1)
        self.application_info.applicationproblem_set.add(app_problem2)

        with self.login(username=self.user.email, password=BaseUserFactory.password):
            data = {"phone": faker.random_number(),
                    "skype": faker.word(),
                    "studies_at": faker.word(),
                    "works_at": faker.word(),
                    "task_field_count": 2,
                    "task_1": faker.url(),
                    "task_2": faker.url()}
            response = self.post('website:apply_course',
                      course_url=self.course_description.url,
                      data=data)

            form = self.get_context('apply_form')
            self.response_200()

        application = Application.objects.filter(user=self.user)
        self.assertEqual(2, ApplicationProblemSolution.objects.filter(application=application).count())

        self.assertEqual(1, application.count())

    def test_applying_for_second_time(self):
        self.assertEqual(0, Application.objects.count())
        application = ApplicationFactory(user=self.user, application_info=self.application_info)

        with self.login(username=self.user.email, password=BaseUserFactory.password):
            data = {}
            response = self.post('website:apply_course',
                      course_url=self.course_description.url,
                      data=data)
            self.assertFalse('apply_form' in response.context)
            self.response_200()
