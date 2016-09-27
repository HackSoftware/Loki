import datetime

from django.core.management import call_command

from test_plus.test import TestCase
from loki.seed.factories import (InterviewerFactory, ApplicationInfoFactory,
                                 ApplicationFactory, CourseFactory,
                                 CourseDescriptionFactory, InterviewFactory)
from loki.applications.models import Application

from ..models import InterviewerFreeTime, Interview


class ChooseInterviewTests(TestCase):
    def test_01_choose_new_interview(self):
        interview = InterviewFactory()
        print(interview.uuid)

        self.assertEqual(1, Interview.objects.count())
