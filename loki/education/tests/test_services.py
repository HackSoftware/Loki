from test_plus.test import TestCase
from django.core.exceptions import ValidationError

from loki.education.services import add_student_to_course, add_teacher_to_course
from loki.education.models import Student, CourseAssignment, Teacher
from loki.seed.factories import (BaseUserFactory, CourseFactory,
                                 CourseAssignmentFactory, TaskFactory,
                                 SolutionFactory)
from loki.base_app.models import BaseUser
from loki.education.services import get_student_data_for_course


class AddStudentToCourseTest(TestCase):

    def setUp(self):
        self.base_user = BaseUserFactory()
        self.course = CourseFactory()

    def test_check_raises_if_student_is_already_teacher_on_this_course(self):
        teacher = BaseUser.objects.promote_to_teacher(self.base_user)
        teacher.teached_courses = [self.course]
        teacher.save()

        with self.assertRaises(ValidationError):
            add_student_to_course(user=teacher, course=self.course)

    def test_raises_errors_if_there_is_courseassingment_for_student(self):
        student = BaseUser.objects.promote_to_student(self.base_user)
        self.assertEqual(1, Student.objects.filter(email=self.base_user.email).count())
        CourseAssignmentFactory(user=student, course=self.course)

        with self.assertRaises(ValidationError):
            add_student_to_course(user=student, course=self.course)

    def test_onboarding_user_if_not_student_and_create_courseassingment(self):
        self.assertEqual(0, Student.objects.filter(email=self.base_user.email).count())

        add_student_to_course(user=self.base_user, course=self.course)

        student = Student.objects.filter(email=self.base_user.email)
        self.assertEqual(1, student.count())
        self.assertEqual(1, CourseAssignment.objects.filter(user=student, course=self.course).count())

    def test_create_courseassingment_for_student(self):
        student = BaseUser.objects.promote_to_student(self.base_user)
        self.assertEqual(1, Student.objects.filter(email=self.base_user.email).count())

        add_student_to_course(user=self.base_user, course=self.course)

        self.assertEqual(1, CourseAssignment.objects.filter(user=student, course=self.course).count())


class AddTeacherToCourseTest(TestCase):

    def setUp(self):
        self.base_user = BaseUserFactory()
        self.course = CourseFactory()

    def test_check_raises_if_teacher_has_courseassingment_for_this_course(self):
        student = BaseUser.objects.promote_to_student(self.base_user)
        CourseAssignmentFactory(user=student,
                                course=self.course)

        with self.assertRaises(ValidationError):
            add_teacher_to_course(user=student, course=self.course)

    def test_check_raises_if_teacher_is_already_teacher_on_this_course(self):
        teacher = BaseUser.objects.promote_to_teacher(self.base_user)
        teacher.teached_courses = [self.course]
        teacher.save()

        with self.assertRaises(ValidationError):
            add_teacher_to_course(user=teacher, course=self.course)

    def test_onboarding_user_if_not_teacher_and_add_course_in_teached_courses(self):
        self.assertEqual(0, Student.objects.filter(email=self.base_user.email).count())

        add_teacher_to_course(user=self.base_user, course=self.course)

        teacher = Teacher.objects.filter(email=self.base_user.email).first()
        self.assertIn(self.course, teacher.teached_courses.all())

    def test_add_course_in_teacher_teached_courses(self):
        teacher = BaseUser.objects.promote_to_teacher(self.base_user)
        self.assertEqual(1, Teacher.objects.filter(email=self.base_user.email).count())

        add_teacher_to_course(user=self.base_user, course=self.course)

        self.assertIn(self.course, teacher.teached_courses.all())


class GetStudentDataForCourse(TestCase):

    PASS = 2
    FAIL = 3

    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()
        self.student = BaseUser.objects.promote_to_student(self.baseuser)
        self.course = CourseFactory()
        self.course_assignment = CourseAssignmentFactory(course=self.course,
                                                         user=self.student)

    def test_course_data_returns_zero_percent_awesome_when_no_solutions(self):
        result_course_data = get_student_data_for_course(self.course_assignment)
        self.assertEqual(0, result_course_data['percent_awesome'])

    def test_course_data_returns_empty_tasks_when_no_solutions(self):
        result_course_data = get_student_data_for_course(self.course_assignment)
        self.assertEqual([], result_course_data['url_tasks'])
        self.assertEqual([], result_course_data['gradable_tasks'])

    def test_course_data_contains_correct_tasks_data(self):
        gradable_task = TaskFactory(course=self.course, gradable=True)
        SolutionFactory(task=gradable_task, student=self.student, status=self.PASS)

        url_task = TaskFactory(course=self.course, gradable=False)
        solution2 = SolutionFactory(task=url_task, student=self.student)
        result_course_data = get_student_data_for_course(self.course_assignment)

        self.assertEqual(1, len(result_course_data['gradable_tasks']))
        self.assertEqual('PASS',
                         result_course_data['gradable_tasks'][0]['solution_status'])
        self.assertEqual(gradable_task.name,
                         result_course_data['gradable_tasks'][0]['name'])

        self.assertEqual(1, len(result_course_data['url_tasks']))
        self.assertEqual(solution2.url,
                         result_course_data['url_tasks'][0]['solution'])
        self.assertEqual(url_task.name,
                         result_course_data['url_tasks'][0]['name'])

        self.assertEqual(result_course_data['percent_awesome'], 100.0)

    def test_course_data_contains_correct_percent_awesome_when_multiple_tasks(self):
        url_task1 = TaskFactory(course=self.course, gradable=False)
        url_task2 = TaskFactory(course=self.course, gradable=False)
        gradable_task1 = TaskFactory(course=self.course, gradable=True)
        gradable_task2 = TaskFactory(course=self.course, gradable=True)

        SolutionFactory(task=url_task1, student=self.student)
        SolutionFactory(task=url_task2, student=self.student)

        SolutionFactory(task=gradable_task1, student=self.student, status=self.PASS)
        SolutionFactory(task=gradable_task2, student=self.student, status=self.FAIL)

        result_course_data = get_student_data_for_course(self.course_assignment)
        self.assertEqual(75.0, result_course_data['percent_awesome'])

    def test_correct_persent_awesome_when_multiple_solutions_of_task(self):
        gradable_task1 = TaskFactory(course=self.course, gradable=True)
        TaskFactory(course=self.course, gradable=False)

        SolutionFactory(task=gradable_task1, student=self.student, status=self.PASS)
        SolutionFactory(task=gradable_task1, student=self.student, status=self.PASS)
        SolutionFactory(task=gradable_task1, student=self.student, status=self.FAIL)
        SolutionFactory(task=gradable_task1, student=self.student, status=self.PASS)

        result_course_data = get_student_data_for_course(self.course_assignment)
        self.assertEqual(50.0, result_course_data['percent_awesome'])
