from datetime import timedelta

from django.utils import timezone

from test_plus.test import TestCase

from seed.factories import (faker,
                            CourseFactory, BaseUserFactory, CourseDescriptionFactory)
from ..models import Application, ApplicationInfo


class TestApplicationViews(TestCase):
    def setUp(self):
        self.course = CourseFactory()
        self.course_description = CourseDescriptionFactory(course=self.course)
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

    def test_applying_for_non_existing_course_should_raise_404(self):
        self.assertEqual(0, Application.objects.count())

        with self.login(username=self.user.email, password=BaseUserFactory.password):
            data = {}
            self.post('website:apply_course',
                      course_url=self.course_description.url + faker.word(),
                      data=data)
            self.response_404()

        self.assertEqual(0, Application.objects.count())
