from datetime import timedelta

from django.utils import timezone

from test_plus.test import TestCase

from seed.factories import CourseFactory
from ..models import ApplicationInfo


class TestApplicationViews(TestCase):
    def setUp(self):
        self.course = CourseFactory()
        self.application_info = ApplicationInfo.objects.create(course=self.course,
                                                               start_date=timezone.now(),
                                                               end_date=timezone.now() + timedelta(1))

    def test_non_registered_user_cannot_apply(self):
        self.get('website:apply_course', course_url=self.course.url)
        self.response_302()
