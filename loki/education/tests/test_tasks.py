from unittest import mock

from test_plus.test import TestCase

from loki.common.utils import make_mock_object
from loki.seed.factories import (
    CourseFactory,
    StudentFactory,
    TaskFactory,
    SolutionFactory,
    ProgrammingLanguageFactory,
    faker
)
from loki.education.models import Solution, SourceCodeTest
from loki.education.tasks import submit_solution


class TasksTests(TestCase):
    def setUp(self):
        self.student = StudentFactory()
        self.course = CourseFactory()

        self.language = ProgrammingLanguageFactory(name='Python')
        self.task = TaskFactory(course=self.course)
        self.test = SourceCodeTest.objects.create(task=self.task,
                                                  language=self.language,
                                                  code='import this')
        self.solution = SolutionFactory(student=self.student,
                                        task=self.task,
                                        status=Solution.SUBMITED)

    @mock.patch('requests.post',
                return_value=make_mock_object(status_code=202,
                                              json=lambda: {'run_id': faker.pyint()},
                                              headers={'Location': faker.url()}))
    @mock.patch('loki.education.tasks.poll_solution', side_effect=lambda *args, **kwargs: None)
    def test_submit_solution_submits_the_solution(self, poll_solution, requests_post):
        submit_solution.delay(self.solution.id)

        self.solution.refresh_from_db()
        self.assertEqual(Solution.PENDING, self.solution.status)

        self.assertTrue(requests_post.called)
