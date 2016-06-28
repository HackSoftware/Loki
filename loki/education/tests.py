from django.core.management import call_command
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from rest_framework.test import APIClient
from base_app.models import BaseUser, Company, City
from education.models import (Student, Certificate, CheckIn, Course, Lecture, Teacher,
                              CourseAssignment, StudentNote, WorkingAt, Task, Solution, Test,
                              SourceCodeTest, ProgrammingLanguage)
from hack_fmi.helper import date_increase, date_decrease
from loki.settings import CHECKIN_TOKEN
from seed import factories
from faker import Factory
import time

faker = Factory.create()


class CheckInTest(TestCase):

    def setUp(self):

        self.student = factories.StudentFactory()

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

        self.check_in_on_start = factories.CheckInFactory(student=self.student)
        self.check_in_on_start.date = date_decrease(29)
        self.check_in_on_start.save()

        self.check_in_after_start = factories.\
            CheckInFactory(student=self.student)
        self.check_in_after_start.date = date_decrease(20)
        self.check_in_after_start.save()

        self.check_in_on_end = factories.CheckInFactory(student=self.student)
        self.check_in_on_end.date = date_decrease(2)
        self.check_in_on_end.save()

        self.check_in_after_course = factories.\
            CheckInFactory(student=self.student)
        self.check_in_after_course.date = date_decrease(1)
        self.check_in_after_course.save()

        self.check_in_before_course = factories.\
            CheckInFactory(student=self.student)
        self.check_in_before_course.date = date_decrease(30)
        self.check_in_before_course.save()

    def test_check_in_with_mac_and_user(self):
        data = {
            'mac': self.student.mac,
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        self.client.post(url, data, format='json')
        self.assertIn(self.student.mac,
                      CheckIn.objects.get(mac=data['mac']).student.mac)

    def test_check_in_with_mac_and_no_user(self):
        data = {
            'mac': faker.mac_address(),
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.client.post(url, data, format='json')

    def test_check_macs_command(self):
        data = {
            'mac': faker.mac_address(),
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        self.client.post(url, data, format='json')
        self.assertIsNone(CheckIn.objects.get(mac=data['mac']).student)
        self.student_no_mac.mac = data['mac']
        self.student_no_mac.save()
        call_command('check_macs')
        self.assertEqual(CheckIn.objects.
                         get(mac=data['mac']).student, self.student_no_mac)

    def test_get_check_ins_for_specific_course(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        data = {
            'student_id': self.student.id,
            'course_id': self.course.id
        }
        url = reverse('education:get_check_ins')
        response = self.client.get(url, data, format='json')
        check_ins = CheckIn.objects.filter(student_id=self.student.id,
                                           date__gte=self.course.start_time,
                                           date__lte=self.course.end_time)
        self.assertEqual(len(response.data), len(check_ins))


class AuthenticationTests(TestCase):

    def setUp(self):
        self.user = factories.BaseUserFactory()

    def test_onboard_student(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        student_count = Student.objects.count()
        baseuser_count = BaseUser.objects.count()
        url = reverse('education:onboard_student')
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.count() - 1, student_count)
        self.assertEqual(BaseUser.objects.count(), baseuser_count)

        self.assertEqual(
            BaseUser.objects.first().email,
            Student.objects.first().email
        )


class UpdateStudentsTests(TestCase):

    def setUp(self):
        self.student = factories.StudentFactory()

    def test_student_update(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        url = reverse('education:student_update')
        data = {'mac': faker.mac_address()}
        self.client.patch(url, data, format='json')

        student = Student.objects.filter(email=self.student.email).first()
        self.assertEqual(student.mac, data['mac'])


class TeachersAPIsTests(TestCase):

    def setUp(self):

        self.course1 = factories.CourseFactory()
        self.course2 = factories.CourseFactory()
        self.course3 = factories.CourseFactory()

        self.lecture1 = factories.LectureFactory(course=self.course1)
        self.lecture2 = factories.LectureFactory(course=self.course2)

        self.teacher = factories.TeacherFactory()

        self.teacher.teached_courses.add(self.course1)
        self.teacher.save()
        self.teacher.teached_courses.add(self.course2)
        self.teacher.save()
        self.student = factories.StudentFactory()
        self.course_assignment = factories.CourseAssignmentFactory(
            user=self.student,
            course=self.course2,
        )
        self.course_assignment2 = factories.CourseAssignmentFactory(
            user=self.student,
            course=self.course3,
        )

    def test_get_courses_api(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        course_count = self.teacher.teached_courses.count()
        url = reverse('education:get_courses')
        response = self.client.get(url, format='json')
        self.assertEqual(course_count, len(response.data))

    def test_get_lectures(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        data = {'course_id': self.course1.id}
        url = reverse('education:get_lectures')
        response = self.client.get(url, data, format='json')
        lectures = Lecture.objects.filter(course=self.course1)
        self.assertEqual(len(response.data), len(lectures))

    def test_create_student_note_valid_data(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        data = {
            'assignment': self.course_assignment.id,
            'text': faker.text()
        }
        url = reverse('education:note')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        note = StudentNote.objects.filter(
            assignment=self.course_assignment).first()
        self.assertEqual(note.text, data['text'])

    def test_create_student_note_invalid_teacher(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        data = {
            'assignment': self.course_assignment2.id,
            'text': faker.text()
        }
        url = reverse('education:note')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)
        note = StudentNote.objects.filter(
            assignment=self.course_assignment2).first()
        self.assertIsNone(note)


class CheckPresenceTests(TestCase):

    def setUp(self):
        self.course1 = factories.CourseFactory(
            start_time=date_decrease(30),
            end_time=date_increase(30),
            generate_certificates_until=date_decrease(1))
        self.course2 = factories.CourseFactory(
            start_time=date_decrease(30),
            end_time=date_increase(30),
            generate_certificates_until=date_decrease(1))

        self.lecture1 = factories.LectureFactory(
            course=self.course1,
            date=date_decrease(1)
        )
        self.lecture2 = factories.LectureFactory(
            course=self.course1,
            date=date_decrease(2)
        )
        self.lecture3 = factories.LectureFactory(
            course=self.course1,
            date=date_decrease(3)
        )

        self.student = factories.StudentFactory()
        self.course_assignment = factories.CourseAssignmentFactory(
            user=self.student,
            course=self.course1,
            student_presence=None
        )
        self.check_in_1 = factories.CheckInFactory(
            student=self.student,
        )
        self.check_in_1.date = date_decrease(1)
        self.check_in_1.save()
        self.check_in_2 = factories.CheckInFactory(
            student=self.student,
        )
        self.check_in_2.date = date_decrease(2)
        self.check_in_2.save()

    def test_command(self):
        self.assertIsNone(self.course_assignment.student_presence)
        call_command('check_presence')
        ca = CourseAssignment.objects.get(id=self.course_assignment.id)
        self.assertEqual(ca.student_presence, 67)


class DropStudentTests(TestCase):

    def setUp(self):
        self.course1 = factories.CourseFactory()
        self.student = factories.StudentFactory(email=faker.email())
        self.course_assignment = factories.CourseAssignmentFactory(
            user=self.student,
            course=self.course1,
            is_attending=True
        )
        self.teacher = factories.TeacherFactory(email=faker.email())
        self.teacher.teached_courses.add(self.course1)
        self.teacher.save()

    def test_drop_student_who_is_attending(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        data = {
            'ca_id': self.course_assignment.id,
            'is_attending': False
        }
        url = reverse('education:drop_student')
        self.assertTrue(self.course_assignment.is_attending)
        self.client.patch(url, data, format='json')
        cass = CourseAssignment.objects.get(id=self.course_assignment.id)
        self.assertFalse(cass.is_attending)


class CheckMacsTests(TestCase):

    def setUp(self):
        self.student = factories.StudentFactory(
            email=faker.email())
        self.student_no_mac = factories.StudentFactory(
            email=faker.email())
        self.check_1 = factories.CheckInFactory(
            student=self.student_no_mac
        )
        self.check_1.date = date_decrease(1)
        self.check_1.save()

        self.check_2 = factories.CheckInFactory(
            mac=self.check_1.mac,
            student=self.student_no_mac
        )
        self.check_2.date = date_decrease(2)
        self.check_2.save()

        self.check_3 = factories.CheckInFactory(
            mac=self.check_1.mac,
            tudent=self.student_no_mac
        )
        self.check_3.date = date_decrease(3)
        self.check_3.save()

    def test_student_enters_mac(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student_no_mac)
        data = {'mac': self.check_1.mac}
        url = reverse('education:student_update')
        self.client.patch(url, data, format='json')
        ch = CheckIn.objects.filter(mac=self.check_1.mac).first()
        self.assertEqual(ch.student, self.student_no_mac)


class TestGetCompanies(TestCase):

    def setUp(self):
        factories.CompanyFactory()
        factories.CompanyFactory()

    def test_get_all_companies(self):
        count = Company.objects.count()
        url = reverse('education:get_companies')
        response = self.client.get(url, format='json')
        self.assertEqual(count, len(response.data))


class TestGetCities(TestCase):

    def setUp(self):
        factories.CityFactory()
        factories.CityFactory()

    def test_get_all_companies(self):
        count = City.objects.count()
        url = reverse('education:get_cities')
        response = self.client.get(url, format='json')
        self.assertEqual(count, len(response.data))


class WorkingAtTests(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            email=faker.email()
        )
        self.company = factories.CompanyFactory()
        self.city = factories.CityFactory()

        self.course = factories.CourseFactory()
        self.course2 = factories.CourseFactory()
        self.course_assignment = factories.CourseAssignmentFactory(
            user=self.student,
            course=self.course,
        )

    def test_post_workingat_creates_instance(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        url = reverse('education:working_at')
        data = {
            'company_name': faker.company(),
            'location': self.city.id,
            'start_date': date_decrease(30),
            'came_working': True,
            'title': faker.job(),
            'course': self.course.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data['location_full']), 2)
        self.assertGreater(len(response.data['course_full']), 0)

    def test_post_workingat_creates_instance_without_course(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        url = reverse('education:working_at')
        data = {
            'company_name': faker.company(),
            'location': self.city.id,
            'start_date': date_decrease(30),
            'came_working': True,
            'title': faker.job(),
            'course': ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_patch_workingat_updates_instance(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        work = factories.WorkingAtFactory(
            student=self.student,
            company=self.company,
            location=self.city,
            course=self.course,
        )

        city2 = factories.CityFactory()
        url = reverse('education:working_at')
        data = {
            'working_at_id': work.id,
            'location': city2.id
        }
        city_before = WorkingAt.objects.first().location.name
        self.client.patch(url, data, format='json')
        city_after = WorkingAt.objects.first().location.name
        self.assertEqual(city_before, self.city.name)
        self.assertEqual(city_after, city2.name)

    def test_patch_workingat_updates_city(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        work = factories.WorkingAtFactory(
            student=self.student,
            company=self.company,
            location=self.city,
            course=self.course,
        )
        city2 = factories.CityFactory()
        url = reverse('education:working_at')
        data = {
            'working_at_id': work.id,
            'location': city2.id,
            'course': self.course2.id
        }
        city_before = WorkingAt.objects.first().location.name
        self.client.patch(url, data, format='json')
        city_after = WorkingAt.objects.first().location.name
        self.assertEqual(city_before, self.city.name)
        self.assertEqual(city_after, city2.name)


class TasksTests(TestCase):

    def setUp(self):
        self.student = factories.StudentFactory(
            email=faker.email(),
        )

        self.course = factories.CourseFactory()

        self.course2 = factories.CourseFactory()

        self.task = factories.TaskFactory(
            course=self.course,
        )

        self.task2 = factories.TaskFactory(
            course=self.course2,
        )

    def test_get_tasks(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        data = {
            "course__id": self.course.id
        }
        url = reverse('education:task')

        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class SolutionsTests(TestCase):

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

        self.test_for_task_with_no_solutions = factories.SourceCodeTestFactory(
            task_id=self.task_with_no_solutions.id,
            language=self.python,
        )
        self.test = factories.SourceCodeTestFactory(
            task_id=self.task.id,
            language=self.python,
        )

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

    def test_teacher_get_all_student_solutions(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        url = reverse('education:student_solutions')
        response = self.client.get(url, format='json')
        self.assertEqual(2, len(response.data))

    def test_teacher_get_student_solutions_for_other_course(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher2)
        url = reverse('education:student_solutions')
        response = self.client.get(url, format='json')
        self.assertEqual(0, len(response.data))

    def test_teacher_get_student_solutions_for_his_course(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher3)
        url = reverse('education:student_solutions')
        response = self.client.get(url, format='json')
        self.assertEqual(1, len(response.data))

    def test_get_solutions(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        url = reverse('education:solution')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(2, len(response.data))

    def test_get_solutions_only_yours(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student2)
        url = reverse('education:solution')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

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

    def test_certificate(self):
        c = Client()

        url = reverse('education:certificate',
                      kwargs={'token': self.certificate.token})

        response = c.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Source Link')
        self.assertContains(response, 'Not sent')


class CourseAsignmentTests(TestCase):

    def setUp(self):
        self.student = factories.StudentFactory(
            email=faker.email(),
        )
        self.course = factories.CourseFactory()
        self.teacher = factories.TeacherFactory(email=faker.email())
        self.teacher.teached_courses.add(self.course)
        self.teacher.save()

    def test_if_data_is_full(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)

        url = reverse('education:get_ca_for_course')
        factories.CourseAssignmentFactory(
            user=self.student,
            course=self.course,)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_if_data_not_full(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)

        url = reverse('education:get_ca_for_course')
        factories.CourseAssignmentFactory(
            user=self.student)

        response = self.client.get(url, format='json')
        self.assertEqual(response.data, [])


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

        # self.grader_request = GraderRequest.objects.create(
        #     request_info="POST /grade",
        #     nonce=105
        # )

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

    '''
    This test checks if a solution with github_url is tested corectly in the grader
    In order to work properly we need to mockup the grader
    A manual check after one run of the test (with correct nounce) showed that the
    code in the grader is the expected one
    '''
    # def test_grading_solution_with_github_link(self):
    #     self.client = APIClient()
    #     self.client.force_authenticate(user=self.student)

    #     task = Task.objects.create(
    #         course=self.course,
    #         description="https://github.com/testasdasdtest/README.md",
    #         name="Task Name 2",
    #         week=1,
    #         gradable=True,
    #     )

    #     self.grader_request = GraderRequest.objects.create(
    #         request_info="POST /grade",
    #         nonce=500
    #     )

    #     test = Test.objects.create(
    #         task=task,
    #         language=self.python,
    #         code="CODE HERE!",
    #         test_type=Test.UNITTEST,
    #         github_url=""
    #     )

    #     url = reverse('education:solution')
    #     data = {
    #         'task': task.id,
    #         'url': 'https://github.com/HackBulgaria/Programming101-Python/blob/master/week02/materials/food_diary.py',
    #     }

    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, 201)

    #     solution = Solution.objects.get(task=task, student=self.student)
    #     self.assertEqual(solution.student, self.student)
    #     self.assertIsNotNone(solution.build_id)
    #     self.assertIsNotNone(solution.check_status_location)

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
