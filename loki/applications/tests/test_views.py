from test_plus.test import TestCase

from loki.seed.factories import (faker, BaseUserFactory, CourseDescriptionFactory, ApplicationProblemFactory,
                                 ApplicationInfoFactory, ApplicationFactory, CourseFactory,
                                 ApplicationProblemSolutionFactory)

from ..models import Application, ApplicationProblemSolution


class TestApplicationViews(TestCase):
    def setUp(self):
        self.course = CourseFactory()
        self.user = BaseUserFactory()
        self.user.is_active = True
        self.user.save()
        self.course_description = CourseDescriptionFactory(course=self.course)
        self.application_info = ApplicationInfoFactory(course=self.course_description)

    def test_non_registered_user_cannot_see_apply_overview(self):
        self.get('applications:apply_overview')
        self.response_200()

    def test_registered_user_can_see_apply_overview(self):
        with self.login(username=self.user.email, password=BaseUserFactory.password):
            self.get('applications:apply_overview')
            self.response_200()

    def test_applying_for_non_existing_course_should_raise_404(self):
        self.assertEqual(0, Application.objects.count())

        with self.login(username=self.user.email, password=BaseUserFactory.password):
            data = {}
            self.post('applications:apply_course',
                      course_url=self.course_description.url + faker.word(),
                      data=data)
            self.response_404()

        self.assertEqual(0, Application.objects.count())

    def test_register_user_can_see_course_apply_form(self):
        with self.login(username=self.user.email, password=BaseUserFactory.password):
            self.get('applications:apply_course', course_url=self.course_description.url)
            self.response_200()

    def test_apply_for_invalid_course_url(self):
        with self.login(username=self.user.email, password=BaseUserFactory.password):
            self.post('applications:edit_application', course_url=faker.word)
            self.response_404()

    def test_applying_for_course_with_inconsistent_data(self):
        self.assertEqual(0, Application.objects.count())

        with self.login(username=self.user.email, password=BaseUserFactory.password):
            data = {"phone": faker.random_number(),
                    "skype": faker.word()}
            self.post('applications:apply_course',
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

            self.post('applications:apply_course',
                      course_url=self.course_description.url,
                      data=data)

            """
            TODO: Finish test
            """
            # form = self.get_context('apply_form')
            self.response_200()

        application = Application.objects.filter(user=self.user)
        self.assertEqual(2, ApplicationProblemSolution.objects.filter(application=application).count())

        self.assertEqual(1, application.count())

    def test_applying_for_the_same_course(self):
        self.assertEqual(0, Application.objects.count())
        ApplicationFactory(user=self.user, application_info=self.application_info)

        with self.login(username=self.user.email, password=BaseUserFactory.password):
            self.post('applications:apply_course',
                      course_url=self.course_description.url)
            self.response_302()

    def test_non_registered_can_not_see_apply_edit(self):
        self.post('applications:edit_application', course_url=self.course_description.url)
        self.response_302()

    def test_registered_user_editing_apply_form(self):
        self.assertEqual(0, Application.objects.count())
        app_problem1 = ApplicationProblemFactory()
        app_problem2 = ApplicationProblemFactory()
        self.application_info.applicationproblem_set.add(app_problem1)
        self.application_info.applicationproblem_set.add(app_problem2)

        application = ApplicationFactory(application_info=self.application_info, user=self.user)
        solution_problem1 = ApplicationProblemSolutionFactory(application=application)
        solution_problem2 = ApplicationProblemSolutionFactory(application=application)

        solution_problem1.problem = app_problem1
        solution_problem1.save()
        solution_problem2.problem = app_problem2
        solution_problem2.save()

        self.assertEqual(1, Application.objects.filter(user=self.user).count())
        self.assertEqual(2, ApplicationProblemSolution.objects.filter(application=application).count())

        with self.login(username=self.user.email, password=BaseUserFactory.password):
            data = {"phone": faker.random_number(),
                    "skype": faker.word(),
                    "studies_at": faker.word(),
                    "works_at": faker.word(),
                    "task_field_count": 2,
                    "task_1": faker.url(),
                    "task_2": faker.url()}

            self.post('applications:edit_application',
                      course_url=self.course_description.url,
                      data=data)

            self.response_200()

        app_problem_solutions = ApplicationProblemSolution.objects.filter(application=application).all()
        self.assertEqual(1, Application.objects.filter(user=self.user).count())
        self.assertEqual(2, app_problem_solutions.count())
        self.assertTrue([solution_problem1, solution_problem2] != app_problem_solutions)
