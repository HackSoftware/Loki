from test_plus.test import TestCase

from loki.education.exceptions import CannotBeStudentForSameCourse, CannotBeTeacherForSameCourse
from loki.education.services import add_student_to_course, add_teacher_to_course
from loki.education.models import Student, CourseAssignment, Teacher
from loki.seed.factories import BaseUserFactory, CourseFactory, CourseAssignmentFactory
from loki.base_app.models import BaseUser


class AddStudentToCourseTest(TestCase):

    def setUp(self):
        self.base_user = BaseUserFactory()
        self.course = CourseFactory()

    def test_check_raises_if_student_is_already_teacher_on_this_course(self):
        teacher = BaseUser.objects.promote_to_teacher(self.base_user)
        teacher.teached_courses = [self.course]
        teacher.save()

        with self.assertRaises(CannotBeStudentForSameCourse):
            add_student_to_course(user=teacher, course=self.course)

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

        with self.assertRaises(CannotBeTeacherForSameCourse):
            add_teacher_to_course(user=student, course=self.course)

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
