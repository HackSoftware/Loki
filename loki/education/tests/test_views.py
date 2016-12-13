from test_plus.test import TestCase

from loki.seed.factories import (BaseUserFactory, CourseFactory, TaskFactory,
                                 CourseAssignmentFactory, SolutionFactory,
                                 MaterialFactory, WeekFactory, LectureFactory)
from loki.base_app.models import BaseUser


class CourseListViewTests(TestCase):

    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()

    def test_not_access_course_list_without_login(self):
        response = self.get('education:course_list')
        self.assertEquals(response.status_code, 302)

    def test_baseuser_not_access_courselist(self):
        with self.login(username=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:course_list')
            self.assertEqual(response.status_code, 403)

    def test_student_can_access_courselist(self):
        student = BaseUser.objects.promote_to_student(self.baseuser)

        with self.login(username=student.email, password=BaseUserFactory.password):
            response = self.get('education:course_list')
            self.assertEqual(response.status_code, 200)

    def test_teacher_can_access_courselist(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)

        with self.login(username=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:course_list')
            self.assertEqual(response.status_code, 200)

    def test_student_can_see_only_courses_for_which_have_courseassignments(self):
        student = BaseUser.objects.promote_to_student(self.baseuser)

        course = CourseFactory()
        course2 = CourseFactory()
        CourseAssignmentFactory(course=course,
                                user=student)

        with self.login(username=student.email, password=BaseUserFactory.password):
            response = self.get('education:course_list')
            self.assertEqual(response.status_code, 200)
            self.assertIn(course, response.context['course_list'])
            self.assertNotIn(course2, response.context['course_list'])

    def test_teacher_can_see_only_courses_for_which_is_teacher(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        course = CourseFactory()
        teacher.teached_courses = [course]
        course2 = CourseFactory()

        with self.login(username=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:course_list')
            self.assertEqual(response.status_code, 200)
            self.assertIn(course, response.context['course_list'])
            self.assertNotIn(course2, response.context['course_list'])


class TaskViewTests(TestCase):

    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()
        self.baseuser2 = BaseUserFactory()
        self.baseuser2.is_active = True
        self.baseuser2.save()
        self.student = BaseUser.objects.promote_to_student(self.baseuser2)
        self.course = CourseFactory()
        self.task = TaskFactory(course=self.course)
        self.course_assignment = CourseAssignmentFactory(course=self.course,
                                                         user=self.student)

    def test_no_access_to_task_list_without_login(self):
        response = self.get('education:task_dashboard', course=self.course.id)
        self.assertEquals(response.status_code, 302)

    def test_baseuser_cannot_access_task_list(self):
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:task_dashboard', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_task_list(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:task_dashboard', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_student_access_task_list(self):
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:task_dashboard', course=self.course.id)
            self.assertEqual(response.status_code, 200)

    def test_student_cannot_access_task_list_of_course_without_tasks(self):
        course2 = CourseFactory()
        CourseAssignmentFactory(course=course2, user=self.student)
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:task_dashboard', course=course2.id)
            self.assertEqual(response.status_code, 404)

    def test_student_see_only_tasks_for_his_course(self):
        task2 = TaskFactory(course=self.course)
        course2 = CourseFactory()
        task_for_course2 = TaskFactory(course=course2)

        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:task_dashboard', course=self.course.id)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.task, response.context['object_list'])
            self.assertIn(task2, response.context['object_list'])
            self.assertNotIn(task_for_course2, response.context['object_list'])


class SolutionViewTests(TestCase):

    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()
        self.baseuser2 = BaseUserFactory()
        self.baseuser2.is_active = True
        self.baseuser2.save()
        self.student = BaseUser.objects.promote_to_student(self.baseuser2)
        self.course = CourseFactory()
        self.task = TaskFactory(course=self.course)
        self.course_assignment = CourseAssignmentFactory(course=self.course,
                                                         user=self.student)

    def test_no_access_to_solution_list_without_login(self):
        response = self.get('education:solution_view', course=self.course.id,
                            task=self.task.id)
        self.assertEquals(response.status_code, 302)

    def test_student_can_access_solution_list_if_has_no_solutions(self):
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:solution_view', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 200)

    def test_baseuser_cannot_access_solution_list_if_has_no_solutions(self):
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:solution_view', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 403)

    def test_student_can_access_solution_list_if_has_solutions(self):
        solution = SolutionFactory(task=self.task, student=self.student)
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:solution_view', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 200)
            self.assertIn(solution, response.context['object_list'])

    def test_baseuser_cannot_access_solution_list_if_has_solutions(self):
        SolutionFactory(task=self.task, student=self.student)
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:solution_view', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_student_solution_list(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        SolutionFactory(task=self.task, student=self.student)

        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:solution_view', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_solution_list_if_no_solutions(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:solution_view', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 403)


class MaterialViewTests(TestCase):

    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()
        self.baseuser2 = BaseUserFactory()
        self.baseuser2.is_active = True
        self.baseuser2.save()
        self.student = BaseUser.objects.promote_to_student(self.baseuser2)
        self.course = CourseFactory()
        self.course_assignment = CourseAssignmentFactory(course=self.course,
                                                         user=self.student)

    def test_no_access_to_solution_list_without_login(self):
        week = WeekFactory()
        LectureFactory(week=week, course=self.course)
        MaterialFactory(week=week, course=self.course)
        response = self.get('education:material_view', course=self.course.id)
        self.assertEquals(response.status_code, 302)

    def test_student_can_access_course_materials(self):
        week = WeekFactory()
        LectureFactory(week=week, course=self.course)
        MaterialFactory(week=week, course=self.course)
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:material_view', course=self.course.id)
            self.assertEqual(response.status_code, 200)

    def test_baseuser_cannot_access_course_materials(self):
        week = WeekFactory()
        LectureFactory(week=week, course=self.course)
        MaterialFactory(week=week, course=self.course)
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:material_view', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_can_access_course_materials(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]
        week = WeekFactory()
        LectureFactory(week=week, course=self.course)
        MaterialFactory(week=week, course=self.course)
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:material_view', course=self.course.id)
            self.assertEqual(response.status_code, 200)

    def test_student_can_access_course_materials_if_no_materials(self):
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:material_view', course=self.course.id)
            self.assertEqual(response.status_code, 200)

    def test_baseuser_cannot_access_course_materials_if_no_materials(self):
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:material_view', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_can_access_course_materials_if_no_materials(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:material_view', course=self.course.id)
            self.assertEqual(response.status_code, 200)

    def test_teacher_cannot_access_no_materials_of_course_not_in_teached_courses(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]
        course2 = CourseFactory()
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:material_view', course=course2.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_materials_of_course_not_in_teached_courses(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]
        week = WeekFactory()
        course2 = CourseFactory()
        LectureFactory(week=week, course=self.course)
        MaterialFactory(week=week, course=self.course)
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:material_view', course=course2.id)
            self.assertEqual(response.status_code, 403)
