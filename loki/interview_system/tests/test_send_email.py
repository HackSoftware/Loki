import datetime

from django.core.management import call_command
from django.core import mail

from test_plus.test import TestCase
from loki.seed.factories import (InterviewerFactory, ApplicationInfoFactory,
                                 ApplicationFactory)
from loki.applications.models import Application

from ..models import InterviewerFreeTime, Interview


class SendEmailForInterviewsTests(TestCase):
    def test_send_email_for_interview_correctly(self):
        app_info = ApplicationInfoFactory()
        application = ApplicationFactory(application_info=app_info)
        interviewer = InterviewerFactory()

        interviewer.courses_to_interview.add(app_info)

        InterviewerFreeTime.objects.create(interviewer=interviewer,
                                           date=datetime.datetime.now().date(),
                                           start_time='11:00',
                                           end_time='14:00')

        self.assertEqual(0, Interview.objects.count())
        self.assertFalse(application.has_interview_date)
        self.assertEquals(1, Application.objects.without_interviews().count())

        call_command('generate_interview_slots')

        application.refresh_from_db()

        self.assertEquals(0, Application.objects.without_interviews().count())
        self.assertTrue(application.has_interview_date)

        call_command('send_emails_for_interviews')

        self.assertEqual(len(mail.outbox), 1)
