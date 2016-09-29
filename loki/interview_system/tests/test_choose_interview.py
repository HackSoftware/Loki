import datetime
from django.test import Client
from django.core.urlresolvers import reverse

from test_plus.test import TestCase
from loki.seed.factories import (InterviewerFactory,
                                 ApplicationFactory,
                                 InterviewFactory,
                                 BaseUserFactory)
from loki.applications.models import Application

from ..models import InterviewerFreeTime, Interview


class ChooseInterviewTests(TestCase):

    def setUp(self):
        self.user = BaseUserFactory()
        self.user.is_active = True
        self.user.save()
        self.client = Client()

    def test_access_choose_new_interview(self):
        confirmed_interviews = Interview.objects.filter(application__isnull=False,
                                                        has_confirmed=False)
        confirmed_interviews_count = confirmed_interviews.count()
        application = ApplicationFactory(user=self.user)
        interview = InterviewFactory(application=application)

        self.assertEqual(confirmed_interviews_count + 1, Interview.objects.count())
        self.assertEqual(interview.application.user, self.user)
        self.client.login(email=self.user.email,
                          password=BaseUserFactory.password)
        url = reverse('interview_system:choose_interview',
                      kwargs={"application": application.id,
                              "interview_token": interview.uuid})

        self.assertEqual(interview.application.id, application.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)



    def test_choose_new_interview(self):
        confirmed_interviews = Interview.objects.filter(application__isnull=False,
                                                        has_confirmed=False)
        self.assertEqual(0, confirmed_interviews.count())

        application = ApplicationFactory(user=self.user)
        interview = InterviewFactory(application=application)

        self.assertEqual(1, Interview.objects.count())
        self.assertEqual(interview.application.user, self.user)
        self.client.login(email=self.user.email,
                          password=BaseUserFactory.password)
        url = reverse('interview_system:choose_interview',
                      kwargs={"application": application.id,
                              "interview_token": interview.uuid})

        self.assertEqual(interview.application.id, application.id)
        free_interview = InterviewFactory(application=None)
        data = {
            'application': application.id,
            'interview_token': free_interview.uuid
        }
        url = reverse('interview_system:choose_interview',
                      kwargs={"application": application.id,
                              "interview_token": free_interview.uuid})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


        self.assertRedirects(response, reverse('interview_system:confirm_interview',
                             kwargs={"application": application.id,
                                     "interview_token": free_interview.uuid}))
