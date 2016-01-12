import time
from django.core.management import call_command
from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from rest_framework.test import APIClient
from base_app.models import Company
from base_app.models import City
from education.models import (Student, Certificate, CheckIn, Course, Lecture, Teacher,
                              CourseAssignment, StudentNote, WorkingAt, Task, Solution,
                              Test, ProgrammingLanguage, GraderRequest)
from hack_fmi.models import BaseUser
from hack_fmi.helper import date_increase, date_decrease
from loki.settings import CHECKIN_TOKEN


class CheckInTest(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12-34-56-78-9A-BC",
        )
        self.teacher = Teacher.objects.create(
            email='teach@teach.bg'
        )
        self.student_no_mac = Student.objects.create(
            email='rado@abv.bg',
        )
        self.course = Course.objects.create(
            description='Test',
            name='Test',
            application_until=date_decrease(30),
            SEO_description='Test',
            SEO_title='Test',
            url='haskell-12',
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )

        self.course_assignment = CourseAssignment.objects.create(
            group_time=1,
            course=self.course,
            user=self.student,
        )

        self.check_in_on_start = CheckIn.objects.create(
            mac="12-34-56-78-9A-BE",
            student=self.student,
        )
        self.check_in_on_start.date = date_decrease(29)
        self.check_in_on_start.save()

        self.check_in_after_start = CheckIn.objects.create(
            mac="12-34-56-78-9A-BE",
            student=self.student,
        )
        self.check_in_after_start.date = date_decrease(20)
        self.check_in_after_start.save()

        self.check_in_on_end = CheckIn.objects.create(
            mac="12-34-56-78-9A-BE",
            student=self.student,
        )
        self.check_in_on_end.date = date_decrease(2)
        self.check_in_on_end.save()

        self.check_in_after_course = CheckIn.objects.create(
            mac="12-34-56-78-9A-BE",
            student=self.student,
        )
        self.check_in_after_course.date = date_decrease(1)
        self.check_in_after_course.save()

        self.check_in_before_course = CheckIn.objects.create(
            mac="12-34-56-78-9A-BE",
            student=self.student,
        )
        self.check_in_before_course.date = date_decrease(30)
        self.check_in_before_course.save()

    def test_check_in_with_mac_and_user(self):
        data = {
            'mac': '12-34-56-78-9A-BC',
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        self.client.post(url, data, format='json')
        self.assertIn(self.student.mac, CheckIn.objects.get(mac='12-34-56-78-9A-BC').student.mac)

    def test_check_in_with_mac_and_no_user(self):
        data = {
            'mac': '12-34-56-78-9A-BA',
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.client.post(url, data, format='json')

    def test_check_macs_command(self):
        data = {
            'mac': '12-34-56-78-9A-BA',
            'token': CHECKIN_TOKEN,
        }
        url = reverse('education:set_check_in')
        self.client.post(url, data, format='json')
        self.assertIsNone(CheckIn.objects.get(mac='12-34-56-78-9A-BA').student)
        self.student_no_mac.mac = '12-34-56-78-9A-BA'
        self.student_no_mac.save()
        call_command('check_macs')
        self.assertEqual(CheckIn.objects.get(mac='12-34-56-78-9A-BA').student, self.student_no_mac)

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
        self.user = BaseUser.objects.create(
            email="test@test.bg",
            first_name="Tester",
            last_name="Testov"
        )

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
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12-34-56-78-9A-BC",
        )

    def test_student_update(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        url = reverse('education:student_update')
        data = {'mac': '01:23:45:67:ab:ab'}
        self.client.patch(url, data, format='json')

        student = Student.objects.filter(email="sten@abv.bg").first()
        self.assertEqual(student.mac, data['mac'])


class TeachersAPIsTests(TestCase):

    def setUp(self):
        self.course1 = Course.objects.create(
            name="Java",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-1/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )
        self.course2 = Course.objects.create(
            name="Python",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-2/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )
        self.course3 = Course.objects.create(
            name="Python3",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-3/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )
        Lecture.objects.create(
            course=self.course1,
            date=date_decrease(8)
        )
        Lecture.objects.create(
            course=self.course1,
            date=date_decrease(10)
        )
        self.teacher = Teacher.objects.create(
            email="ivo@ivo.bg",
        )
        self.teacher.teached_courses.add(self.course1)
        self.teacher.save()
        self.teacher.teached_courses.add(self.course2)
        self.teacher.save()
        self.student = Student.objects.create(
            email="stud@abv.bg",
            mac="60:67:20:cc:b1:62"
        )
        self.course_assignment = CourseAssignment.objects.create(
            user=self.student,
            course=self.course2,
            group_time=1
        )
        self.course_assignment2 = CourseAssignment.objects.create(
            user=self.student,
            course=self.course3,
            group_time=1
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
            'text': 'Very good student!'
        }
        url = reverse('education:note')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        note = StudentNote.objects.filter(assignment=self.course_assignment).first()
        self.assertEqual(note.text, 'Very good student!')

    def test_create_student_note_invalid_teacher(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        data = {
            'assignment': self.course_assignment2.id,
            'text': 'Very good student!'
        }
        url = reverse('education:note')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 403)
        note = StudentNote.objects.filter(assignment=self.course_assignment2).first()
        self.assertIsNone(note)


class CheckPresenceTests(TestCase):

    def setUp(self):
        self.course1 = Course.objects.create(
            name="Java",
            application_until=date_decrease(31),
            url="https://hackbulgaria.com/course/haskell-1/",
            start_time=date_decrease(30),
            end_time=date_increase(30),
            generate_certificates_until=date_decrease(1),
        )
        self.course2 = Course.objects.create(
            name="Python",
            application_until=date_decrease(31),
            url="https://hackbulgaria.com/course/haskell-2/",
            start_time=date_decrease(30),
            end_time=date_increase(30),
            generate_certificates_until=date_decrease(1),
        )
        Lecture.objects.create(
            course=self.course1,
            date=date_decrease(1)
        )
        Lecture.objects.create(
            course=self.course1,
            date=date_decrease(2)
        )
        Lecture.objects.create(
            course=self.course1,
            date=date_decrease(3)
        )

        self.student = Student.objects.create(
            email="stud@abv.bg",
            mac="60:67:20:cc:b1:62"
        )
        self.course_assignment = CourseAssignment.objects.create(
            user=self.student,
            course=self.course1,
            group_time=1
        )
        self.check_in_1 = CheckIn.objects.create(
            mac="12:34:56:78:9A:BE",
            student=self.student,
        )
        self.check_in_1.date = date_decrease(1)
        self.check_in_1.save()
        self.check_in_2 = CheckIn.objects.create(
            mac="12:34:56:78:9A:BE",
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
        self.course1 = Course.objects.create(
            name="Java",
            application_until="2015-06-20",
            url="https://hackbulgaria.com/course/haskell-1/",
            start_time=date_decrease(30),
            end_time=date_increase(30),
            generate_certificates_until=date_decrease(1),
        )
        self.student = Student.objects.create(
            email="stud@abv.bg",
            mac="60:67:20:cc:b1:62"
        )
        self.course_assignment = CourseAssignment.objects.create(
            user=self.student,
            course=self.course1,
            group_time=1,
            is_attending=True
        )
        self.teacher = Teacher.objects.create(
            email="ivo@ivo.bg",
        )
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
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12:34:56:78:9A:BC",
        )
        self.student_no_mac = Student.objects.create(
            email='rado@abv.bg',
        )
        self.check_1 = CheckIn.objects.create(
            mac="12:34:56:78:9A:BE",
        )
        self.check_1.date = date_decrease(1)
        self.check_1.save()

        self.check_2 = CheckIn.objects.create(
            mac="12:34:56:78:9A:BE",
        )
        self.check_2.date = date_decrease(2)
        self.check_2.save()

        self.check_3 = CheckIn.objects.create(
            mac="12:34:56:78:9A:BE",
        )
        self.check_3.date = date_decrease(3)
        self.check_3.save()

    def test_student_enters_mac(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student_no_mac)
        data = {'mac': '12:34:56:78:9A:BE'}
        url = reverse('education:student_update')
        self.client.patch(url, data, format='json')
        ch = CheckIn.objects.filter(mac='12:34:56:78:9A:BE').first()
        self.assertEqual(ch.student, self.student_no_mac)


class TestGetCompanies(TestCase):

    def setUp(self):
        Company.objects.create(
            name="com"
        )
        Company.objects.create(
            name="coma"
        )

    def test_get_all_companies(self):
        count = Company.objects.count()
        url = reverse('education:get_companies')
        response = self.client.get(url, format='json')
        self.assertEqual(count, len(response.data))


class TestGetCities(TestCase):

    def setUp(self):
        City.objects.create(
            name="com"
        )
        City.objects.create(
            name="coma"
        )

    def test_get_all_companies(self):
        count = City.objects.count()
        url = reverse('education:get_cities')
        response = self.client.get(url, format='json')
        self.assertEqual(count, len(response.data))


class WorkingAtTests(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12:34:56:78:9A:BC",
        )
        self.company = Company.objects.create(
            name="HackBulgaria"
        )
        self.city = City.objects.create(
            name="Sofia"
        )
        self.course = Course.objects.create(
            name="Java",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-1/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )
        self.course2 = Course.objects.create(
            name="Python",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-2/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )
        self.course_assignment = CourseAssignment.objects.create(
            group_time=1,
            course=self.course,
            user=self.student,
        )

    def test_post_workingat_creates_instance(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        url = reverse('education:working_at')
        data = {
            'company_name': "Hackbulgaria",
            'location': self.city.id,
            'start_date': date_decrease(30),
            'came_working': True,
            'title': 'Developer',
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
            'company_name': "Hackbulgaria",
            'location': self.city.id,
            'start_date': date_decrease(30),
            'came_working': True,
            'title': 'Developer',
            'course': ""
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_patch_workingat_updates_instance(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)
        work = WorkingAt.objects.create(
            student=self.student,
            company_name='HackBulgaria',
            location=self.city,
            start_date=date_decrease(30),
            title='Developer',
            course=self.course
        )
        city2 = City.objects.create(
            name='Plovdiv'
        )
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
        work = WorkingAt.objects.create(
            student=self.student,
            company_name='HackBulgaria',
            location=self.city,
            start_date=date_decrease(30),
            title='Developer',
            course=self.course
        )
        city2 = City.objects.create(
            name='Plovdiv'
        )
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
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12:34:56:78:9A:BC",
        )

        self.course = Course.objects.create(
            name="Java",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-1/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )

        self.course2 = Course.objects.create(
            name="Java2",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/asd-1/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )

        self.task = Task.objects.create(
            course=self.course,
            description="https://github.com/lqlq/README.md",
            name="Task Name",
            week=1,
        )

        self.task2 = Task.objects.create(
            course=self.course2,
            description="https://github.com/lololo/README.md",
            name="Task Name 2",
            week=1,
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
        self.student = Student.objects.create(
            email='sten@abv.bg',
            mac="12:34:56:78:9A:BC",
        )

        self.student2 = Student.objects.create(
            email='ivo@abv.bg',
            mac="12:34:56:78:9A:B1",
        )

        self.course = Course.objects.create(
            name="Java",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-1/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )

        self.course2 = Course.objects.create(
            name="Python",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskelsl-1/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )

        self.assignment = CourseAssignment.objects.create(
            user=self.student,
            course=self.course,
            group_time=1,
        )

        self.task = Task.objects.create(
            course=self.course,
            description="https://github.com/lqlq/README.md",
            name="Task Name",
            week=1,
            gradable=False,
        )

        self.task_with_no_solutions = Task.objects.create(
            course=self.course,
            description="https://github.com/lqlnkmbq/README.md",
            name="Task Name 1",
            week=1,
            gradable=False,
        )

        self.python = ProgrammingLanguage.objects.create(
            name="python"
        )

        self.test_for_task_with_no_solutions = Test.objects.create(
            task=self.task_with_no_solutions,
            language=self.python,
            code="CODE HERE!",
            test_type=Test.UNITTEST,
            github_url=""
        )

        self.test = Test.objects.create(
            task=self.task,
            language=self.python,
            code="CODE HERE!",
            test_type=Test.UNITTEST,
            github_url=""
        )

        self.solution = Solution.objects.create(
            student=self.student,
            task=self.task,
            url='https://github.com/lqdsadaslsq/solution.py',
        )

        self.solution2 = Solution.objects.create(
            student=self.student2,
            task=self.task,
            url='https://github.com/lololo/solution.py',
        )

        self.certificate = Certificate.objects.create(
            assignment=self.assignment,
        )

        self.teacher = Teacher.objects.create(
            email="testteacher@testteacher.bg",
        )

        self.teacher.teached_courses.add(self.course)
        self.teacher.teached_courses.add(self.course2)
        self.teacher.save()

        self.teacher2 = Teacher.objects.create(
            email="testteacher2@testteacher2.bg",
        )

        self.teacher2.teached_courses.add(self.course2)
        self.teacher.save()

    def test_teacher_get_student_solutions(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher)
        # course_count = self.teacher.teached_courses.count()
        url = reverse('education:student_solutions')
        response = self.client.get(url, format='json')
        self.assertNotEqual(0, len(response.data))

    def test_teacher_get_student_solutions_for_other_course(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.teacher2)
        # course_count = self.teacher.teached_courses.count()
        url = reverse('education:student_solutions')
        response = self.client.get(url, format='json')
        self.assertEqual(0, len(response.data))

    def test_get_solutions(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)

        url = reverse('education:solution')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_solutions_only_yours(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student2)

        url = reverse('education:solution')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_post_solutions(self):
        logged_student = self.student2
        self.client = APIClient()
        self.client.force_authenticate(user=logged_student)

        url = reverse('education:solution')
        data = {
            'task': self.task_with_no_solutions.id,
            'url': 'https://github.com/lolo/solution.py'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_post_incorrect_code_solution(self):
        logged_student = self.student2
        self.client = APIClient()
        self.client.force_authenticate(user=logged_student)

        url = reverse('education:solution')
        data = "{'submitted':true,'status':null,'task':147,'code':'asdf','url':null}"

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_solution_with_incorrect_github_url(self):
        logged_student = self.student2
        self.client = APIClient()
        self.client.force_authenticate(user=logged_student)

        url = reverse('education:solution')
        data = {
            'task': self.task_with_no_solutions.id,
            'url': 'sdsadqweqwesda'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

        url = reverse('education:solution')
        data = {
            'task': self.task_with_no_solutions.id,
            'url': 'https://docs.angularjs.org/api/ng/directive/select'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

        url = reverse('education:solution')
        data = {
            'task': self.task_with_no_solutions.id,
            'url': 'https://github.com/HackBulgaria/Programming101-Python'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_post_solutions_filter(self):
        logged_student = self.student

        course2 = Course.objects.create(
            name="Java2",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/Javata-1/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )

        task2 = Task.objects.create(
            course=course2,
            description="https://github.com/lqddlq/README.md",
            name="Task3 Name",
            week=1,
            gradable=False,
        )

        Solution.objects.create(
            student=logged_student,
            task=task2,
            url='https://github.com/lqdddsadaslsq/solution.py',
        )

        self.client = APIClient()
        self.client.force_authenticate(user=logged_student)

        url = reverse('education:solution')
        data = {
            'task__course__id': course2.id
        }

        response = self.client.get(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Solution.objects.filter(student=logged_student).count(), 2)
        self.assertEqual(len(response.data), 1)

    def test_certificate(self):
        c = Client()
        url = reverse('education:certificate', kwargs={'pk': self.certificate.id})
        response = c.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Source Link')
        self.assertContains(response, 'Not sent')

# class CourseAsignmentTests(TestCase):

#     def setUp(self):
#         self.student = Student.objects.create(
#             email='kosta@abv.bg',
#             mac="12:34:56:78:9A:BC",
#         )
#         self.course = Course.objects.create(
#             name="Java2",
#             application_until=date_decrease(30),
#             url="https://hackbulgaria.com/course/Javata-1/",
#             start_time=date_decrease(29),
#             end_time=date_decrease(2),
#             generate_certificates_until=date_decrease(1),
#         )

#     def test_if_data_not_full(self):
#         logged_student = self.student
#         self.client = APIClient()
#         self.client.force_authenticate(user=logged_student)

#         url = reverse('education:course_assignment')

#         data = {
#             'course__id': self.course.id
#         }

#         response = self.client.patch(url, data, format='json')
#         self.assertEqual(response.status_code, 403)

#     def test_if_data_is_full(self):
#         logged_student = self.student
#         self.client = APIClient()
#         self.client.force_authenticate(user=logged_student)

#         url = reverse('education:course_assignment')

#         data = {
#             'student_presence': 1,
#             'user': self.student.id,
#             'studentnote_set': "",
#         }

#         response = self.client.patch(url, data, format='json')
#         print(response.data)
#         self.assertEqual(response.status_code, 200)


class TestSolutionTests(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            email='test@test.com',
            mac="12:34:56:78:9A:BC",
        )

        self.course = Course.objects.create(
            name="Java",
            application_until=date_decrease(30),
            url="https://hackbulgaria.com/course/haskell-1/",
            start_time=date_decrease(29),
            end_time=date_decrease(2),
            generate_certificates_until=date_decrease(1),
        )

        self.assignment = CourseAssignment.objects.create(
            user=self.student,
            course=self.course,
            group_time=1,
        )

        self.task = Task.objects.create(
            course=self.course,
            description="https://github.com/testasdasdtest/README.md",
            name="Task Name 1",
            week=1,
            gradable=False,
        )

        self.python = ProgrammingLanguage.objects.create(
            name="python"
        )

        # self.grader_request = GraderRequest.objects.create(
        #     request_info="POST /grade",
        #     nonce=105
        # )

        self.test = Test.objects.create(
            task=self.task,
            language=self.python,
            code="CODE HERE!",
            test_type=Test.UNITTEST,
            github_url=""
        )

    def test_grader_response(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.student)

        url = reverse('education:solution')
        data = {
            'task': self.task.id,
            'url': 'https://github.com/testsolutionasdtest/solution.py',
            'code': "print('da')",
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


    # def test_solution_status(self):
    #     self.client = APIClient()
    #     self.client.force_authenticate(user=self.student)

    #     url = reverse('education:solution')
    #     data = {
    #         'task': self.task.id,
    #         'url': 'https://github.com/testsolutionasdtest/solution.py',
    #         'code': "print('da')",
    #     }

    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, 201)

    #     solution = Solution.objects.get(task=self.task, student=self.student)
    #     url = reverse('education:solution_status', kwargs={'pk': solution.id})
    #     time.sleep(6)
    #     response = self.client.get(url, format='json')
