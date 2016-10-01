import datetime
import uuid
from django.test import Client
from django.core.urlresolvers import reverse

from test_plus.test import TestCase
from loki.seed.factories import (InterviewerFactory,
                                 ApplicationFactory,
                                 InterviewFactory,
                                 BaseUserFactory)
from loki.applications.models import Application

from ..models import Interview


class ChooseInterviewTests(TestCase):

    def setUp(self):
        self.user = BaseUserFactory()
        self.user.is_active = True
        self.user.save()
        self.application = ApplicationFactory(user=self.user)
        self.interview = InterviewFactory(application=self.application,
                                          has_confirmed=False)
        self.client = Client()

    def test_access_choose_new_interview(self):
        confirmed_interviews = Interview.objects.filter(application__isnull=False,
                                                        has_confirmed=True)
        confirmed_interviews_count = confirmed_interviews.count()

        self.assertEqual(confirmed_interviews_count + 1, Interview.objects.count())
        self.assertEqual(self.interview.application.user, self.user)
        self.client.login(email=self.user.email,
                          password=BaseUserFactory.password)
        url = reverse('interview_system:choose_interview',
                      kwargs={"application": self.application.id,
                              "interview_token": self.interview.uuid})

        self.assertEqual(self.interview.application.id, self.application.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)



    def test_choose_new_interview(self):
        confirmed_interviews = Interview.objects.filter(application__isnull=False,
                                                        has_confirmed=True)
        confirmed_interviews_count = confirmed_interviews.count()
        self.assertEqual(0, confirmed_interviews.count())

        self.assertEqual(self.interview.application.user, self.user)
        self.client.login(email=self.user.email,
                          password=BaseUserFactory.password)
        url = reverse('interview_system:choose_interview',
                      kwargs={"application": self.application.id,
                              "interview_token": self.interview.uuid})

        self.assertEqual(self.interview.application.id, self.application.id)
        free_interview = InterviewFactory(application=None)
        data = {
            'application': self.application.id,
            'interview_token': free_interview.uuid
        }
        url = reverse('interview_system:choose_interview',
                      kwargs={"application": self.application.id,
                              "interview_token": free_interview.uuid})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


        self.assertRedirects(response, reverse('interview_system:confirm_interview',
                             kwargs={"application": self.application.id,
                                     "interview_token": free_interview.uuid}))

    def test_access_confirm_interview(self):
        with self.login(username=self.user.email, password=BaseUserFactory.password):
            url = reverse('interview_system:confirm_interview',
                          kwargs={"application": self.application.id,
                                  "interview_token": self.interview.uuid})

            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_confirm_interview_from_confirm_page(self):
        with self.login(username=self.user.email, password=BaseUserFactory.password):
            url = reverse('interview_system:confirm_interview',
                          kwargs={"application": self.application.id,
                                  "interview_token": self.interview.uuid})

            response = self.client.post(url)
            self.assertEqual(response.status_code, 200)
            self.interview.refresh_from_db()

            self.assertEqual(self.interview.has_confirmed,True)

    def test_unsigned_user_access_confirm_page(self):
        url = reverse('interview_system:confirm_interview',
                      kwargs={"application": self.application.id,
                              "interview_token": self.interview.uuid})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_unsigned_user_access_choose_page(self):
        url = reverse('interview_system:choose_interview',
                      kwargs={"application": self.application.id,
                              "interview_token": self.interview.uuid})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_choose_new_interview_after_already_confirmed(self):
        with self.login(username=self.user.email, password=BaseUserFactory.password):
            self.post('interview_system:confirm_interview', self.application.id,
                        self.interview.uuid)
            self.interview.refresh_from_db()
            self.assertEqual(Interview.objects.filter(
                             has_confirmed=True).count(), 1)

            response = self.get('interview_system:choose_interview',
                                self.application.id,
                                self.interview.uuid, follow=True)

            red_url = reverse('interview_system:confirm_interview',
                          kwargs={"application": self.application.id,
                                  "interview_token": self.interview.uuid})

            self.assertRedirects(response, red_url)

    def test_confirm_non_existing_interview(self):
        uuid1 = uuid.uuid4()
        self.assertEqual(self.interview.uuid != uuid1, True)
        with self.login(username=self.user.email, password=BaseUserFactory.password):
            response = self.get('interview_system:confirm_interview',
                                    self.application.id, uuid1)
            self.assertEqual(response.status_code, 404)

    def test_confirm_non_existing_application(self):
        uuid1 = uuid.uuid4()
        app = ApplicationFactory(has_interview_date=False)
        self.assertEqual(self.application.user != app.user, True)
        with self.login(username=self.user.email, password=BaseUserFactory.password):
            response = self.get('interview_system:confirm_interview',
                                    app.id, self.interview.uuid)
            self.assertEqual(response.status_code, 404)

    def test_access_confirm_from_user_without_application(self):
        user_without_app = BaseUserFactory()
        user_without_app.is_active = True
        user_without_app.save()
        with self.login(username=user_without_app.email,
                        password=BaseUserFactory.password):
            response = self.get('interview_system:confirm_interview',
                                    self.application.id, self.interview.uuid)
            self.assertEqual(response.status_code, 404)
