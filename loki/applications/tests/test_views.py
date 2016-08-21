from datetime import timedelta

from django.utils import timezone

from test_plus.test import TestCase

from seed.factories import faker, CourseFactory, BaseUserFactory
from ..models import ApplicationInfo


class TestApplicationViews(TestCase):
    def setUp(self):
        self.course = CourseFactory()
        self.application_info = ApplicationInfo.objects.create(course=self.course,
                                                               start_date=timezone.now(),
                                                               end_date=timezone.now() + timedelta(1))
        self.user = BaseUserFactory()
        self.user.is_active = True
        self.user.save()

    def test_non_registered_user_cannot_see_apply_overview(self):
        self.get('website:apply_overview')
        self.response_302()

    def test_registered_user_can_see_apply_overview(self):
        with self.login(username=self.user.email, password=BaseUserFactory.password):
            self.get('website:apply_overview')
            self.response_200()
