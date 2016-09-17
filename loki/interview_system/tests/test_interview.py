import datetime

from django.core.management import call_command

from test_plus.test import TestCase
from loki.seed.factories import InterviewerFactory, ApplicationInfoFactory, ApplicationFactory
from loki.applications.models import Application

from ..models import InterviewerFreeTime, Interview


class InterviewGenerationTests(TestCase):
    def test_interviews_are_generated_correctly(self):
        app_info = ApplicationInfoFactory()
        application = ApplicationFactory(application_info=app_info)
        interviewer = InterviewerFactory()

        interviewer.courses_to_interview.add(app_info)

        free_time = InterviewerFreeTime.objects.create(interviewer=interviewer,
                                                       date=datetime.datetime.now().date(),
                                                       start_time='11:00',
                                                       end_time='14:00')

        self.assertEqual(0, Interview.objects.count())
        self.assertFalse(application.has_interview_date)
        self.assertEquals(1, Application.objects.without_interviews().count())

        call_command('generate_interview_slots')

        self.assertEqual(1, Interview.objects.filter(application__isnull=False).count())
        self.assertEquals(0, Application.objects.without_interviews().count())


    def test_interviews_are_generated_correctly_if_new_application_is_added_after_generation(self):
        app_info = ApplicationInfoFactory()
        ApplicationFactory(application_info=app_info)
        interviewer = InterviewerFactory()

        interviewer.courses_to_interview.add(app_info)

        free_time = InterviewerFreeTime.objects.create(interviewer=interviewer,
                                                       date=datetime.datetime.now().date(),
                                                       start_time='11:00',
                                                       end_time='14:00')

        self.assertEquals(1, Application.objects.without_interviews().count())
        call_command('generate_interview_slots')
        self.assertEquals(5, Interview.objects.get_free_slots().count())
        self.assertEquals(0, Application.objects.without_interviews().count())


        application = ApplicationFactory(application_info=app_info)
        self.assertEquals(1, Application.objects.without_interviews().count())

        call_command('generate_interview_slots')
        self.assertEquals(4, Interview.objects.get_free_slots().count())
        self.assertEquals(0, Application.objects.without_interviews().count())
