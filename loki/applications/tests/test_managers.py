from test_plus.test import TestCase
from ..models import Application
from loki.seed.factories import ApplicationFactory, ApplicationInfoFactory


class ApplicationManagerTests(TestCase):

    def test_counting_applications_without_interviews(self):
        self.assertEquals(0, Application.objects.count())
        self.assertEquals(0, Application.objects.without_interviews().count())
        app_info_1 = ApplicationInfoFactory()

        ApplicationFactory(application_info=app_info_1)
        ApplicationFactory(application_info=app_info_1)

        self.assertEquals(2, Application.objects.without_interviews().count())
