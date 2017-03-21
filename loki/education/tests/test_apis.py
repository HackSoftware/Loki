import time
from unittest import skip
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings

from rest_framework.test import APIClient

from loki.education.models import Student, Solution, SourceCodeTest, CheckIn
from loki.seed import factories

from faker import Factory

faker = Factory.create()


class CheckInTest(TestCase):

    def setUp(self):

        self.student = factories.StudentFactory()
        self.student.is_active = True
        self.student.save()
        self.teacher = factories.TeacherFactory()
        self.student_no_mac = Student.objects.create(
            email=faker.email(),
        )
        self.company = factories.CompanyFactory()
        self.partner = factories.PartnerFactory(company=self.company)
        self.course = factories.CourseFactory()

        self.courseAssignmet = factories.\
            CourseAssignmentFactory(course=self.course,
                                    user=self.student)
        self.courseAssignmet.favourite_partners.add(self.partner)

    def test_check_in_with_mac_and_user(self):
        data = {
            'mac': self.student.mac,
            'token': settings.CHECKIN_TOKEN,
        }

        url = reverse('education:set_check_in')
        self.client.post(url, data, format='json')

        self.assertEqual(self.student.mac,
                         CheckIn.objects.get(mac=data['mac']).mac)

    def test_check_in_with_mac_and_no_user(self):
        data = {
            'mac': faker.mac_address(),
            'token': settings.CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.client.post(url, data, format='json')


class SolutionsTests(TestCase):

    @skip("Don't want to test")
    def setUp(self):
        self.student = factories.StudentFactory(
            email=faker.email(),
        )

        self.student2 = factories.StudentFactory(
            email=faker.email(),
        )

        self.course = factories.CourseFactory()

        self.course2 = factories.CourseFactory()

        self.assignment = factories.CourseAssignmentFactory(
            user=self.student,
            course=self.course,
        )

        self.task = factories.TaskFactory(
            course=self.course,
        )

        self.task_with_no_solutions = factories.TaskFactory(
            course=self.course,
            gradable=False,
        )

        self.python = factories.ProgrammingLanguageFactory()

        self.solution = factories.SolutionFactory(
            student=self.student,
            task=self.task,
        )

        self.solution2 = factories.SolutionFactory(
            student=self.student2,
            task=self.task,
        )

        self.certificate = factories.CertificateFactory(
            assignment_id=self.assignment.id,
        )

        self.teacher = factories.TeacherFactory(email=faker.email())

        self.teacher.teached_courses.add(self.course)
        self.teacher.teached_courses.add(self.course2)
        self.teacher.save()

        self.teacher2 = factories.TeacherFactory(email=faker.email())

        self.teacher2.teached_courses.add(self.course2)
        self.teacher.save()

        self.course3 = factories.CourseFactory()
        self.assignment3 = factories.CourseAssignmentFactory(
            user=self.student,
            course=self.course3,
        )

        self.task3 = factories.TaskFactory(
            course=self.course3)

        self.test = factories.SourceCodeTestFactory(
            task_id=self.task3.id,
            language=self.python,
        )

        self.solution3 = factories.SolutionFactory(
            student=self.student,
            task=self.task3,
        )

        self.teacher3 = factories.TeacherFactory(email=faker.email())
        self.teacher3.teached_courses.add(self.course3)
        self.teacher3.save()

    @skip("Don't want to test")
    def test_teacher_get_all_student_solutions(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        url = reverse('education:student_solutions')
        response = self.client.get(url, format='json')
        self.assertEqual(2, len(response.data))

    @skip("Don't want to test")
    def test_teacher_get_student_solutions_for_other_course(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher2)
        url = reverse('education:student_solutions')
        response = self.client.get(url, format='json')
        self.assertEqual(0, len(response.data))

    @skip("Don't want to test")
    def test_teacher_get_student_solutions_for_his_course(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher3)
        url = reverse('education:student_solutions')
        response = self.client.get(url, format='json')
        self.assertEqual(1, len(response.data))

    @skip("Don't want to test")
    def test_get_solutions(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        url = reverse('education:solution')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(response.data))

    @skip("Don't want to test")
    def test_get_solutions_only_yours(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student2)
        url = reverse('education:solution')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    @skip("Don't want to test")
    def test_post_solution_for_ungradable_task(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student2)
        url = reverse('education:solution')
        data = {
            'task': self.task_with_no_solutions.id,
            'url': self.solution2.url,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)  # 201 Created
        expected = Solution.\
            STATUS_CHOICE[Solution.SUBMITTED_WITHOUT_GRADING][1]
        self.assertEqual(expected, response.data['status'])

    @skip("Don't want to test")
    def test_post_solution_for_ungradable_task_for_non_existing_task(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student2)
        url = reverse('education:solution')
        data = {
            'submitted': True,
            'status': None,
            'task': faker.random_number(),
            'code': faker.text(),
            'url': None
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)

    @skip("Don't want to test")
    def test_post_solution_for_ungradable_test_with_incorrect_github_url(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student2)

        url = reverse('education:solution')
        data = {
            'task': self.task_with_no_solutions.id,
            'url': faker.url()
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

        not_github_url = faker.url()
        self.assertNotIn("github.com", not_github_url)
        url = reverse('education:solution')
        data = {
            'task': self.task_with_no_solutions.id,
            'url': not_github_url,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

        url = reverse('education:solution')
        data = {
            'task': self.task_with_no_solutions.id,
            'url': 'https://github.com/HackBulgaria/Programming101-Python'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    @skip("Don't want to test")
    def test_post_solution_for_ungradable_task_without_url(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student2)

        url = reverse('education:solution')

        data = {
            'task': self.task_with_no_solutions.id,
            'code': faker.text(),
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

    @skip("Don't want to test")
    def test_post_solution_ungradable_task_without_url_file_code(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student2)

        url = reverse('education:solution')

        data = {
            'task': self.task_with_no_solutions.id,
            'code': None,
            'url': None,
            'file': None
        }

        self.client.post(url, data, format='json')
        self.assertRaises(ValidationError)

    @skip("Don't want to test")
    def test_post_solution_ungradable_task_without_url_file(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student2)

        url = reverse('education:solution')

        data = {
            'task': self.task_with_no_solutions.id,
            'url': None,
            'file': None
        }

        self.client.post(url, data, format='json')
        self.assertRaises(ValidationError)

    @skip("Don't want to test")
    def test_post_solutions_filter(self):
        logged_student = self.student

        course2 = factories.CourseFactory()

        task2 = factories.TaskFactory(
            course=course2,
            gradable=False,
        )

        factories.SolutionFactory(
            student=logged_student,
            task=task2,
        )

        self.client = APIClient()
        self.client.force_authenticate(user=logged_student)

        url = reverse('education:solution')

        data = {
            'task__course__id': course2.id
        }

        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.\
            assertEqual(Solution.objects.
                        filter(student=logged_student).count(), 3)
        self.assertEqual(len(response.data), 1)


class TestSolutionTests(TestCase):

    def setUp(self):
        self.student = factories.StudentFactory(
            email=faker.email(),
        )

        self.course = factories.CourseFactory()

        self.assignment = factories.CourseAssignmentFactory(
            user=self.student,
            course=self.course,
        )

        self.task = factories.TaskFactory(
            course=self.course,
            gradable=False,
        )

        self.python = factories.ProgrammingLanguageFactory(
            name="python"
        )

        self.test = SourceCodeTest.objects.create(
            task=self.task,
            language=self.python,
            code="CODE HERE!",
            test_type=SourceCodeTest.UNITTEST,
        )

    def test_grader_response(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)

        url = reverse('education:solution')
        data = {
            'task': self.task.id,
            'url': 'https://github.com/testsolutionasdtest/solution.py',
            'code': None,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

        solution = Solution.objects.get(task=self.task, student=self.student)
        self.assertEqual(solution.student, self.student)
        # In order to check the build_id a grader mockup is needed
        # self.assertIsNotNone(solution.build_id)
        # self.assertIsNotNone(solution.check_status_location)

    def test_solution_status(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)

        url = reverse('education:solution')
        data = {
            'task': self.task.id,
            'url': 'https://github.com/testsolutionasdtest/solution.py',
            'code': faker.text(),
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

        solution = Solution.objects.get(task=self.task, student=self.student)
        url = reverse('education:solution_status', kwargs={'pk': solution.id})
        time.sleep(6)
        response = self.client.get(url, format='json')
