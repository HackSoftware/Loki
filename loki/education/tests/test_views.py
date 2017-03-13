from datetime import datetime, timedelta
from test_plus.test import TestCase

from loki.seed.factories import (BaseUserFactory, CourseFactory, TaskFactory,
                                 CourseAssignmentFactory, SolutionFactory,
                                 MaterialFactory, WeekFactory, LectureFactory,
                                 CheckInFactory)
from loki.base_app.models import BaseUser
from loki.education.models import StudentNote

from faker import Factory
faker = Factory.create()


class CourseListViewTests(TestCase):

    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()

    def test_not_access_course_list_without_login(self):
        response = self.get('education:course-list')
        self.assertEquals(response.status_code, 302)

    def test_baseuser_not_access_courselist(self):
        with self.login(username=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:course-list')
            self.assertEqual(response.status_code, 403)

    def test_student_can_access_courselist(self):
        student = BaseUser.objects.promote_to_student(self.baseuser)

        with self.login(username=student.email, password=BaseUserFactory.password):
            response = self.get('education:course-list')
            self.assertEqual(response.status_code, 200)

    def test_teacher_can_access_courselist(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)

        with self.login(username=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:course-list')
            self.assertEqual(response.status_code, 200)

    def test_student_can_see_only_courses_for_which_have_courseassignments(self):
        student = BaseUser.objects.promote_to_student(self.baseuser)

        course = CourseFactory()
        course2 = CourseFactory()
        CourseAssignmentFactory(course=course,
                                user=student)

        with self.login(username=student.email, password=BaseUserFactory.password):
            response = self.get('education:course-list')
            self.assertEqual(response.status_code, 200)
            self.assertIn(course, response.context['student_courses'])
            self.assertNotIn(course2, response.context['student_courses'])

            self.assertNotIn('teacher_courses', response.context)

    def test_teacher_can_see_only_courses_for_which_is_teacher(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        course = CourseFactory()
        teacher.teached_courses = [course]
        course2 = CourseFactory()

        with self.login(username=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:course-list')
            self.assertEqual(response.status_code, 200)
            self.assertIn(course, response.context['teacher_courses'])
            self.assertNotIn(course2, response.context['teacher_courses'])

            self.assertNotIn('student_courses', response.context)

    def test_common_teacher_and_student_user_can_see_courses_for_which_ca_or_is_teacher(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        student = BaseUser.objects.promote_to_student(self.baseuser)

        course = CourseFactory()
        teacher.teached_courses = [course]

        course2 = CourseFactory()
        CourseAssignmentFactory(course=course2,
                                user=student)

        with self.login(username=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:course-list')
            self.assertEqual(response.status_code, 200)
            self.assertIn(course, response.context['teacher_courses'])
            self.assertNotIn(course2, response.context['teacher_courses'])
            self.assertIn(course2, response.context['student_courses'])
            self.assertNotIn(course, response.context['student_courses'])


class TaskListViewTests(TestCase):

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
        response = self.get('education:task-list', course=self.course.id)
        self.assertEquals(response.status_code, 302)

    def test_baseuser_cannot_access_task_list(self):
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:task-list', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_task_list(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:task-list', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_student_access_task_list(self):
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:task-list', course=self.course.id)
            self.assertEqual(response.status_code, 200)

    def test_student_cannot_access_task_list_of_course_without_tasks(self):
        course2 = CourseFactory()
        CourseAssignmentFactory(course=course2, user=self.student)
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:task-list', course=course2.id)
            self.assertEqual(response.status_code, 404)

    def test_student_see_only_tasks_for_his_course(self):
        task2 = TaskFactory(course=self.course)
        course2 = CourseFactory()
        task_for_course2 = TaskFactory(course=course2)

        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:task-list', course=self.course.id)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.task, response.context['object_list'])
            self.assertIn(task2, response.context['object_list'])
            self.assertNotIn(task_for_course2, response.context['object_list'])

    def test_cannot_submit_solutions_if_date_is_not_in_deadline(self):
        self.course.deadline_date = datetime.now().date() - timedelta(days=2)
        self.course.save()

        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:task-list', course=self.course.id)
            self.assertEqual(response.status_code, 404)


class SolutionListViewTests(TestCase):

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
        response = self.get('education:solution-list', course=self.course.id,
                            task=self.task.id)
        self.assertEquals(response.status_code, 302)

    def test_student_can_access_solution_list_if_has_no_solutions(self):
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:solution-list', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 200)

    def test_baseuser_cannot_access_solution_list_if_has_no_solutions(self):
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:solution-list', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 403)

    def test_student_can_access_solution_list_if_has_solutions(self):
        solution = SolutionFactory(task=self.task, student=self.student)
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:solution-list', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 200)
            self.assertIn(solution, response.context['object_list'])

    def test_baseuser_cannot_access_solution_list_if_has_solutions(self):
        SolutionFactory(task=self.task, student=self.student)
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:solution-list', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_student_solution_list(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        SolutionFactory(task=self.task, student=self.student)

        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:solution-list', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_solution_list_if_no_solutions(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:solution-list', course=self.course.id,
                                task=self.task.id)
            self.assertEqual(response.status_code, 403)


class TeacherTaskListViewTests(TestCase):

    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()
        self.teacher = BaseUser.objects.promote_to_teacher(self.baseuser)

        self.baseuser2 = BaseUserFactory()
        self.baseuser2.is_active = True
        self.baseuser2.save()
        self.student = BaseUser.objects.promote_to_student(self.baseuser2)
        self.course = CourseFactory()
        self.course_assignment = CourseAssignmentFactory(course=self.course,
                                                         user=self.student)
        self.task = TaskFactory(course=self.course)

    def test_no_access_to_task_list_without_login(self):
        response = self.get('education:student-task-list', course=self.course.id, student=faker.random_int())
        self.assertEquals(response.status_code, 302)

    def test_baseuser_cannot_access_task_list(self):
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:student-task-list', course=self.course.id, student=faker.random_int())
            self.assertEqual(response.status_code, 403)

    def test_student_cannot_access_task_list(self):
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:student-task-list', course=self.course.id, student=self.student.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_course_student_task_list_if_he_doesnt_teach_it(self):
        with self.login(email=self.teacher.email, password=BaseUserFactory.password):
            response = self.get('education:student-task-list', course=self.course.id, student=self.student.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_can_access_course_student_task_list_if_he_teaches_it(self):
        self.teacher.teached_courses = [self.course]

        with self.login(email=self.teacher.email, password=BaseUserFactory.password):
            response = self.get('education:student-task-list', course=self.course.id, student=self.student.id)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.task, response.context['object_list'])

    def test_teacher_can_see_student_task_only_course_if_he_teaches_it(self):
        course2 = CourseFactory()
        TaskFactory(course=course2)
        self.teacher.teached_courses = [self.course]

        with self.login(email=self.teacher.email, password=BaseUserFactory.password):
            response = self.get('education:student-task-list', course=course2.id, student=self.student.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_can_see_student_task_list_only_if_he_teaches_course(self):
        course2 = CourseFactory()
        task2 = TaskFactory(course=course2)
        self.teacher.teached_courses = [self.course]

        with self.login(email=self.teacher.email, password=BaseUserFactory.password):
            response = self.get('education:student-task-list', course=self.course.id, student=self.student.id)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.task, response.context['object_list'])
            self.assertNotIn(task2, response.context['object_list'])


class TeacherSolutionListViewTests(TestCase):

    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()
        self.teacher = BaseUser.objects.promote_to_teacher(self.baseuser)

        self.baseuser2 = BaseUserFactory()
        self.baseuser2.is_active = True
        self.baseuser2.save()
        self.student = BaseUser.objects.promote_to_student(self.baseuser2)
        self.course = CourseFactory()
        self.course_assignment = CourseAssignmentFactory(course=self.course,
                                                         user=self.student)
        self.task = TaskFactory(course=self.course)
        self.task2 = TaskFactory(course=self.course)

    def test_no_access_to_solution_list_without_login(self):
        response = self.get('education:student-solution-list', course=self.course.id,
                            student=self.student.id, task=self.task.id)
        self.assertEquals(response.status_code, 302)

    def test_baseuser_cannot_access_solution_list(self):
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:student-solution-list', course=self.course.id,
                                student=self.student.id, task=self.task.id)
            self.assertEqual(response.status_code, 403)

    def test_student_cannot_access_solution_list(self):
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:student-solution-list', course=self.course.id,
                                student=self.student.id, task=self.task.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_course_student_solution_list_if_he_doesnt_teach_it(self):
        with self.login(email=self.teacher.email, password=BaseUserFactory.password):
            response = self.get('education:student-solution-list', course=self.course.id,
                                student=self.student.id, task=self.task.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_can_access_course_student_solution_list_if_he_teach_it(self):
        self.teacher.teached_courses = [self.course]
        solution = SolutionFactory(task=self.task, student=self.student)
        solution2 = SolutionFactory(task=self.task, student=self.student)

        with self.login(email=self.teacher.email, password=BaseUserFactory.password):
            response = self.get('education:student-solution-list', course=self.course.id,
                                student=self.student.id, task=self.task.id)
            self.assertEqual(response.status_code, 200)
            self.assertIn(solution, response.context['object_list'])
            self.assertIn(solution, response.context['solution_list'])
            self.assertIn(solution2, response.context['object_list'])
            self.assertIn(solution2, response.context['solution_list'])

class MaterialListViewTests(TestCase):

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

    def test_no_access_to_material_list_without_login(self):
        week = WeekFactory()
        LectureFactory(week=week, course=self.course)
        MaterialFactory(week=week, course=self.course)
        response = self.get('education:material-list', course=self.course.id)
        self.assertEquals(response.status_code, 302)

    def test_student_can_access_course_materials(self):
        week = WeekFactory()
        LectureFactory(week=week, course=self.course)
        MaterialFactory(week=week, course=self.course)
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:material-list', course=self.course.id)
            self.assertEqual(response.status_code, 200)

    def test_student_cannot_access_other_courses_materials(self):
        course2 = CourseFactory()
        week = WeekFactory()
        LectureFactory(week=week, course=course2)
        MaterialFactory(week=week, course=course2)
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:material-list', course=course2.id)
            self.assertEqual(response.status_code, 403)

    def test_baseuser_cannot_access_course_materials(self):
        week = WeekFactory()
        LectureFactory(week=week, course=self.course)
        MaterialFactory(week=week, course=self.course)
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:material-list', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_can_access_course_materials(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]
        week = WeekFactory()
        LectureFactory(week=week, course=self.course)
        MaterialFactory(week=week, course=self.course)
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:material-list', course=self.course.id)
            self.assertEqual(response.status_code, 200)

    def test_student_can_access_course_materials_if_no_materials(self):
        with self.login(email=self.student.email, password=BaseUserFactory.password):
            response = self.get('education:material-list', course=self.course.id)
            self.assertEqual(response.status_code, 200)

    def test_baseuser_cannot_access_course_materials_if_no_materials(self):
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:material-list', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_can_access_course_materials_if_no_materials(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:material-list', course=self.course.id)
            self.assertEqual(response.status_code, 200)

    def test_teacher_cannot_access_no_materials_of_course_not_in_teached_courses(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]
        course2 = CourseFactory()
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:material-list', course=course2.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_materials_of_course_not_in_teached_courses(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]
        week = WeekFactory()
        course2 = CourseFactory()
        LectureFactory(week=week, course=self.course)
        MaterialFactory(week=week, course=self.course)
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:material-list', course=course2.id)
            self.assertEqual(response.status_code, 403)


class StudentListViewTests(TestCase):

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

    def test_cannot_access_student_list_if_no_login(self):
        response = self.get('education:student-list', course=self.course.id)
        self.assertEquals(response.status_code, 302)

    def test_student_cannot_access_student_list(self):
        with self.login(email=self.student.email, password=BaseUserFactory.password):

            response = self.get('education:student-list', course=self.course.id)
            self.assertEquals(response.status_code, 403)

    def test_teacher_can_access_student_list(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:student-list', course=self.course.id)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.course_assignment, response.context['object_list'])

    def test_teacher_cannot_access_student_list_if_not_teached_it(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:student-list', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_can_see_student_list_only_for_his_course(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]

        baseuser3 = BaseUserFactory()
        baseuser3.is_active = True
        baseuser3.save()
        student = BaseUser.objects.promote_to_student(baseuser3)
        course2 = CourseFactory()
        course_assignment_for_baseuser3 = CourseAssignmentFactory(course=course2,
                                                                  user=student)

        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:student-list', course=self.course.id)
            self.assertEqual(response.status_code, 200)
            self.assertIn(self.course_assignment, response.context['object_list'])
            self.assertNotIn(course_assignment_for_baseuser3, response.context['object_list'])


class CourseDetailViewTests(TestCase):

    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()
        self.teacher = BaseUser.objects.promote_to_teacher(self.baseuser)

        self.baseuser2 = BaseUserFactory()
        self.baseuser2.is_active = True
        self.baseuser2.save()
        self.student = BaseUser.objects.promote_to_student(self.baseuser2)
        self.course = CourseFactory()
        self.course_assignment = CourseAssignmentFactory(course=self.course,
                                                         user=self.student)
        self.task = TaskFactory(course=self.course, gradable=True)

    def test_not_access_course_detail_without_login(self):
        response = self.get('education:course-detail', course=self.course.id,)
        self.assertEquals(response.status_code, 302)

    def test_baseuser_cannot_access_course_detail(self):
        with self.login(username=self.baseuser.email, password=BaseUserFactory.password):
            response = self.get('education:course-detail', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_student_cannot_access_course_detail(self):
        student = BaseUser.objects.promote_to_student(self.baseuser)

        with self.login(username=student.email, password=BaseUserFactory.password):
            response = self.get('education:course-detail', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_access_course_detail_if_he_is_not_teacher(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)

        with self.login(username=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:course-detail', course=self.course.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_can_access_course_detail_if_he_is_teacher(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]

        with self.login(username=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:course-detail', course=self.course.id)
            self.assertEqual(response.status_code, 200)

    def test_teacher_can_see_only_his_course(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]
        course2 = CourseFactory()

        with self.login(username=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:course-detail', course=course2.id)
            self.assertEqual(response.status_code, 403)

    def test_check_count_gradable_and_notgradable_tasks(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]

        SolutionFactory(task=self.task,
                        student=self.student)
        TaskFactory(course=self.course, gradable=False)

        with self.login(username=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:course-detail', course=self.course.id)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(1, response.context['not_gradable_tasks'])
            self.assertEqual(1, response.context['gradable_tasks'])
            self.assertEqual(1, response.context['count_solutions'])

    def test_check_count_gradable_and_notgradable_solutions(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]

        solution1 = SolutionFactory(task=self.task,
                                    student=self.student)
        solution1.status = 3
        solution1.save()

        solution2 = SolutionFactory(task=self.task,
                                    student=self.student)
        solution2.status = 2
        solution2.save()

        url_task = TaskFactory(course=self.course, gradable=False)
        SolutionFactory(task=url_task,
                        student=self.student)

        with self.login(username=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:course-detail', course=self.course.id)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(1, response.context['not_gradable_tasks'])
            self.assertEqual(1, response.context['gradable_tasks'])
            self.assertEqual(3, response.context['count_solutions'])
            self.assertEqual(1, response.context['not_gradable_tasks'])
            self.assertEqual(1, response.context['passed_solutions'])
            self.assertEqual(1, response.context['url_solutions'])
            self.assertEqual(1, response.context['failed_solutions'])


class CreateStudentNoteTests(TestCase):

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

    def test_cannot_create_student_notes_if_no_login(self):
        response = self.post('education:student-note-create', course=self.course.id)
        self.assertEquals(response.status_code, 302)

    def test_student_cannot_create_student_notes(self):
        with self.login(email=self.student.email, password=BaseUserFactory.password):

            response = self.post('education:student-note-create', course=self.course.id)
            self.assertEquals(response.status_code, 403)

    def test_base_cannot_create_student_notes(self):
        with self.login(email=self.baseuser.email, password=BaseUserFactory.password):

            response = self.post('education:student-note-create', course=self.course.id)
            self.assertEquals(response.status_code, 403)

    def test_teacher_can_create_student_notes(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]

        with self.login(email=teacher.email, password=BaseUserFactory.password):
            data = {'text': faker.text(),
                    'assignment': self.course_assignment.id}
            response = self.post('education:student-note-create', course=self.course.id, data=data, follow=True)
            self.assertEquals(response.status_code, 200)

        self.assertEqual(1, StudentNote.objects.filter(assignment=self.course_assignment).count())
        self.assertEqual(teacher, StudentNote.objects.filter(assignment=self.course_assignment).first().author)


class StudentDetailView(TestCase):
    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()
        self.baseuser2 = BaseUserFactory()
        self.baseuser2.is_active = True
        self.baseuser2.save()
        self.student = BaseUser.objects.promote_to_student(self.baseuser2)
        self.student.mac = "22:44:55:66:77"
        self.course = CourseFactory()
        self.ca = CourseAssignmentFactory(course=self.course,
                                          user=self.student)
        self.task = TaskFactory(course=self.course, gradable=True)
        self.baseuser3 = BaseUserFactory()
        self.baseuser3.is_active = True
        self.baseuser3.save()

    def test_cannot_access_student_list_if_no_login(self):
        response = self.get('education:student-detail', course=self.course.id, ca=self.ca.id)
        self.assertEquals(response.status_code, 302)

    def test_student_cannot_access_student_list(self):
        with self.login(email=self.student.email, password=BaseUserFactory.password):

            response = self.get('education:student-detail', course=self.course.id, ca=self.ca.id)
            self.assertEquals(response.status_code, 403)

    def test_teacher_can_see_student_detail_information(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]

        solution1 = SolutionFactory(task=self.task,
                                    student=self.student)
        solution1.status = 3
        solution1.save()

        solution2 = SolutionFactory(task=self.task,
                                    student=self.student)
        solution2.status = 2
        solution2.save()

        solution3 = SolutionFactory(task=self.task,
                                    student=self.student)
        solution3.status = 2
        solution3.save()

        url_task = TaskFactory(course=self.course, gradable=False)
        SolutionFactory(task=url_task,
                        student=self.student)

        LectureFactory(course=self.course,
                       date=datetime.now().date() - timedelta(days=9))

        LectureFactory(course=self.course,
                       date=datetime.now().date() - timedelta(days=7))

        LectureFactory(course=self.course,
                       date=datetime.now().date() - timedelta(days=5))

        LectureFactory(course=self.course,
                       date=datetime.now().date() - timedelta(days=3))

        check_in1 = CheckInFactory(mac=self.student.mac,
                                   user=self.student)
        check_in1.date = datetime.now().date() - timedelta(days=9)
        check_in1.save()
        check_in2 = CheckInFactory(mac=self.student.mac,
                                   user=self.student)
        check_in2.date = datetime.now().date() - timedelta(days=7)
        check_in2.save()

        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:student-detail', course=self.course.id, ca=self.ca.id)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.ca, response.context['object'])
            self.assertEqual(2, response.context['passed_solutions'])
            self.assertEqual(1, response.context['failed_solutions'])
            self.assertEqual(1, response.context['url_solutions'])

    def test_teacher_cannot_see_other_students_detail_information(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser)
        teacher.teached_courses = [self.course]

        other_student = BaseUser.objects.promote_to_student(self.baseuser3)
        other_student_course = CourseFactory()
        other_student_ca = CourseAssignmentFactory(course=other_student_course,
                                                   user=other_student)

        self.assertFalse(other_student_course in teacher.teached_courses.all())

        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.get('education:student-detail', course=other_student_course.id,
                                ca=other_student_ca.id)
            self.assertEqual(response.status_code, 403)


class DropStudentTests(TestCase):

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

    def test_cannot_drop_student_if_not_logged_in(self):
        response = self.post('education:drop-student',
                             course=self.course.id,
                             ca=self.course_assignment.id)
        self.assertEqual(response.status_code, 302)

    def test_non_teachers_cannot_drop_student(self):
        with self.login(email=self.baseuser2.email, password=BaseUserFactory.password):
            response = self.post('education:drop-student',
                                 course=self.course.id,
                                 ca=self.course_assignment.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_cannot_drop_students_from_other_courses(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser2)

        course = CourseFactory()
        teacher.teached_courses = [course]
        teacher.save()

        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.post('education:drop-student',
                                 course=self.course.id,
                                 ca=self.course_assignment.id)
            self.assertEqual(response.status_code, 403)

    def test_teacher_can_drop_student_from_course_if_he_teaches_it(self):
        teacher = BaseUser.objects.promote_to_teacher(self.baseuser2)
        teacher.teached_courses = [self.course]
        teacher.save()

        self.assertTrue(self.course_assignment.is_attending)
        with self.login(email=teacher.email, password=BaseUserFactory.password):
            response = self.post('education:drop-student',
                                 course=self.course.id,
                                 ca=self.course_assignment.id)
            self.assertEqual(response.status_code, 302)

        self.course_assignment.refresh_from_db()
        self.assertFalse(self.course_assignment.is_attending)
