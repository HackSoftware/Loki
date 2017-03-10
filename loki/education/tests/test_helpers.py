from test_plus.test import TestCase

from loki.education.helper import calculate_student_progress_for_course_in_percents
from loki.education.models import Student, CourseAssignment, Teacher, Task, Solution
from loki.seed.factories import (BaseUserFactory, CourseFactory, CourseAssignmentFactory,
                                 TaskFactory, SolutionFactory)
from loki.base_app.models import BaseUser


class CalculatePercentAwesomeTest(TestCase):

    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()
        self.student = BaseUser.objects.promote_to_student(self.baseuser)
        self.course = CourseFactory()
        self.course_assignment = CourseAssignmentFactory(course=self.course,
                                                         user=self.student)

        self.gradable_tasks = TaskFactory.create_batch(10, course=self.course, gradable=True)
        self.url_tasks = TaskFactory.create_batch(10, course=self.course, gradable=False)

    def test_percent_awesome_when_added_solutions_only_for_gradable_tasks(self):
        for task in self.gradable_tasks:
            solution = SolutionFactory(task=task, status=2, student=self.student)

        self.assertEqual(10, Solution.objects.all().count())
        self.assertEqual(50, calculate_student_progress_for_course_in_percents(self.course_assignment))


    def test_percent_awesome_when_added_everything(self):
        for task in self.gradable_tasks:
            solution = SolutionFactory(task=task, status=2, student=self.student)

        for task in self.url_tasks:
            solution = SolutionFactory(task=task, student=self.student)

        self.assertEqual(20, Solution.objects.all().count())
        self.assertEqual(100, calculate_student_progress_for_course_in_percents(self.course_assignment))

    def test_percent_awesome_when_there_are_failed_solutions(self):
        for task in self.gradable_tasks[0:5]:
            solution = SolutionFactory(task=task, status=2, student=self.student)

        for task in self.gradable_tasks[5:10]:
            solution = SolutionFactory(task=task, status=1, student=self.student)

        for task in self.url_tasks[0:5]:
            solution = SolutionFactory(task=task, student=self.student)

        self.assertEqual(15, Solution.objects.all().count())
        self.assertEqual(50, calculate_student_progress_for_course_in_percents(self.course_assignment))
