import factory

from test_plus.test import TestCase
from ..models import Application
from loki.seed.factories import (ApplicationFactory, ApplicationInfoFactory,
                                 CourseFactory, CourseDescriptionFactory)


class ApplicationManagerTests(TestCase):

    def test_counting_applications_without_interviews(self):
        self.assertEquals(0, Application.objects.count())
        self.assertEquals(0, Application.objects.without_interviews().count())
        app_info_1 = ApplicationInfoFactory()

        ApplicationFactory(application_info=app_info_1)
        ApplicationFactory(application_info=app_info_1)

        self.assertEquals(2, Application.objects.without_interviews().count())

    def test_counting_applications_for_app_info_without_interviews(self):
        course1, course2 = factory.build_batch(size=2, klass=CourseFactory)
        cd1 = CourseDescriptionFactory(course=course1)
        cd2 = CourseDescriptionFactory(course=course2)
        app_info1 = ApplicationInfoFactory(course=cd1)
        app_info2 = ApplicationInfoFactory(course=cd2)

        self.assertEquals(0, Application.objects.without_interviews_for(app_info1).count())
        self.assertEquals(0, Application.objects.without_interviews_for(app_info2).count())

        ApplicationFactory(application_info=app_info1)
        ApplicationFactory(application_info=app_info1)
        ApplicationFactory(application_info=app_info1)
        ApplicationFactory(application_info=app_info1)
        ApplicationFactory(application_info=app_info2)
        ApplicationFactory(application_info=app_info2)

        self.assertEquals(4, Application.objects.without_interviews_for(app_info1).count())
        self.assertEquals(2, Application.objects.without_interviews_for(app_info2).count())
        self.assertEquals(6, Application.objects.without_interviews().count())
