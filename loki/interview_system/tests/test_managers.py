import datetime

from test_plus.test import TestCase
from ..models import InterviewerFreeTime, Interview
from loki.seed.factories import (ApplicationFactory, ApplicationInfoFactory,
                                 InterviewerFactory)


class InterviewManagerTests(TestCase):

    def test_counting_interview_slots_without_applications(self):
        app_info = ApplicationInfoFactory()
        interviewer = InterviewerFactory()
        interviewer.courses_to_interview.add(app_info)

        free_time = InterviewerFreeTime.objects.create(interviewer=interviewer,
                                                       date=datetime.datetime.now().date(),
                                                       start_time='11:00',
                                                       end_time='14:00')

        interview = Interview.objects.create(interviewer=interviewer,
                                             date=datetime.datetime.now().date(),
                                             start_time='11:00',
                                             end_time='11:30',
                                             interviewer_time_slot=free_time)

        Interview.objects.create(interviewer=interviewer,
                                 date=datetime.datetime.now().date(),
                                 start_time='12:00',
                                 end_time='12:30',
                                 interviewer_time_slot=free_time)

        self.assertEquals(2, Interview.objects.get_free_slots().count())

        application = ApplicationFactory(application_info=app_info)
        interview.application = application
        interview.save()

        self.assertEquals(1, Interview.objects.get_free_slots().count())

    def test_counting_confirmed_interviews_with_app_info(self):
        app_info = ApplicationInfoFactory()
        application1 = ApplicationFactory(application_info=app_info)
        application2 = ApplicationFactory(application_info=app_info)
        application3 = ApplicationFactory(application_info=app_info)

        interviewer = InterviewerFactory()
        interviewer.courses_to_interview.add(app_info)

        free_time = InterviewerFreeTime.objects.create(interviewer=interviewer,
                                                       date=datetime.datetime.now().date(),
                                                       start_time='11:00',
                                                       end_time='14:00')

        self.assertEquals(0, Interview.objects.confirmed_for(app_info).count())
        Interview.objects.create(interviewer=interviewer,
                                 application=application1,
                                 date=datetime.datetime.now().date(),
                                 start_time='11:00',
                                 end_time='11:30',
                                 interviewer_time_slot=free_time,
                                 has_confirmed=True)

        Interview.objects.create(interviewer=interviewer,
                                 application=application2,
                                 date=datetime.datetime.now().date(),
                                 start_time='12:00',
                                 end_time='12:30',
                                 interviewer_time_slot=free_time,
                                 has_confirmed=True)

        Interview.objects.create(interviewer=interviewer,
                                 application=application3,
                                 date=datetime.datetime.now().date(),
                                 start_time='12:00',
                                 end_time='12:30',
                                 interviewer_time_slot=free_time)

        self.assertEquals(2, Interview.objects.confirmed_for(app_info).count())
