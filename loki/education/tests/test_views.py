from test_plus.test import TestCase

from loki.seed.factories import BaseUserFactory
from loki.base_app.models import BaseUser


class CourseListViewTests(TestCase):

    def setUp(self):
        self.baseuser = BaseUserFactory()
        self.baseuser.is_active = True
        self.baseuser.save()

    def test_not_access_course_list_without_login(self):
        response = self.get('interview_system:generate_interviews')
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
