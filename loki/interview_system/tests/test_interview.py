import datetime

from django.core.management import call_command

from test_plus.test import TestCase
from loki.seed.factories import (InterviewerFactory, ApplicationInfoFactory,
                                 ApplicationFactory, CourseFactory,
                                 CourseDescriptionFactory)
from loki.applications.models import Application

from ..models import InterviewerFreeTime, Interview


class InterviewGenerationTests(TestCase):
    def test_interviews_are_generated_correctly(self):
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

        self.assertEqual(1, Interview.objects.filter(application__isnull=False).count())
        self.assertEquals(0, Application.objects.without_interviews().count())

    def test_interviews_are_generated_correctly_if_new_application_is_added_after_generation(self):
        app_info = ApplicationInfoFactory()
        ApplicationFactory(application_info=app_info)
        interviewer = InterviewerFactory()

        interviewer.courses_to_interview.add(app_info)

        InterviewerFreeTime.objects.create(interviewer=interviewer,
                                           date=datetime.datetime.now().date(),
                                           start_time='11:00',
                                           end_time='14:00')

        self.assertEquals(1, Application.objects.without_interviews().count())
        call_command('generate_interview_slots')
        self.assertEquals(5, Interview.objects.get_free_slots().count())
        self.assertEquals(0, Application.objects.without_interviews().count())

        ApplicationFactory(application_info=app_info)
        self.assertEquals(1, Application.objects.without_interviews().count())

        call_command('generate_interview_slots')
        self.assertEquals(4, Interview.objects.get_free_slots().count())
        self.assertEquals(0, Application.objects.without_interviews().count())

    def test_generate_interviews_for_more_interviewers(self):
        app_info = ApplicationInfoFactory()
        application1 = ApplicationFactory(application_info=app_info)
        application2 = ApplicationFactory(application_info=app_info)
        application3 = ApplicationFactory(application_info=app_info)
        interviewer1 = InterviewerFactory()
        interviewer2 = InterviewerFactory()

        interviewer1.courses_to_interview.add(app_info)
        interviewer2.courses_to_interview.add(app_info)

        InterviewerFreeTime.objects.create(interviewer=interviewer1,
                                           date=datetime.datetime.now().date(),
                                           start_time='11:00',
                                           end_time='14:00')

        InterviewerFreeTime.objects.create(interviewer=interviewer2,
                                           date=datetime.datetime.now().date(),
                                           start_time='12:00',
                                           end_time='15:00')

        self.assertEquals(3, Application.objects.without_interviews().count())

        call_command('generate_interview_slots')
        self.assertEquals(9, Interview.objects.get_free_slots().count())
        interviewer_for_app1 = Interview.objects.get(application=application1).interviewer
        interviewer_for_app2 = Interview.objects.get(application=application2).interviewer
        interviewer_for_app3 = Interview.objects.get(application=application3).interviewer
        self.assertNotEqual(interviewer_for_app1, interviewer_for_app2)
        self.assertEqual(interviewer_for_app1, interviewer_for_app3)
        self.assertEquals(0, Application.objects.without_interviews().count())

    def test_generate_interviews_for_different_courses_with_different_interviewers(self):
        course1 = CourseFactory()
        course2 = CourseFactory()
        cd1 = CourseDescriptionFactory(course=course1)
        cd2 = CourseDescriptionFactory(course=course2)
        app_info1 = ApplicationInfoFactory(course=cd1)
        app_info2 = ApplicationInfoFactory(course=cd2)

        application1 = ApplicationFactory(application_info=app_info1)
        application2 = ApplicationFactory(application_info=app_info2)
        application3 = ApplicationFactory(application_info=app_info1)
        application4 = ApplicationFactory(application_info=app_info2)
        application5 = ApplicationFactory(application_info=app_info1)
        interviewer1 = InterviewerFactory()
        interviewer2 = InterviewerFactory()
        interviewer3 = InterviewerFactory()

        interviewer1.courses_to_interview.add(app_info1)
        interviewer2.courses_to_interview.add(app_info2)
        interviewer3.courses_to_interview.add(app_info1)

        InterviewerFreeTime.objects.create(interviewer=interviewer1,
                                           date=datetime.datetime.now().date(),
                                           start_time='11:00',
                                           end_time='14:00')
        InterviewerFreeTime.objects.create(interviewer=interviewer2,
                                           date=datetime.datetime.now().date(),
                                           start_time='12:00',
                                           end_time='15:00')
        InterviewerFreeTime.objects.create(interviewer=interviewer3,
                                           date=datetime.datetime.now().date(),
                                           start_time='13:00',
                                           end_time='15:00')

        self.assertEquals(5, Application.objects.without_interviews().count())

        call_command('generate_interview_slots')
        self.assertEquals(11, Interview.objects.get_free_slots().count())

        interviewer_for_app1 = Interview.objects.get(application=application1).interviewer
        interviewer_for_app2 = Interview.objects.get(application=application2).interviewer
        interviewer_for_app3 = Interview.objects.get(application=application3).interviewer
        interviewer_for_app4 = Interview.objects.get(application=application4).interviewer
        interviewer_for_app5 = Interview.objects.get(application=application5).interviewer

        self.assertEqual(interviewer1, interviewer_for_app1)
        self.assertEqual(interviewer1, interviewer_for_app5)
        self.assertEqual(interviewer2, interviewer_for_app2)
        self.assertEqual(interviewer2, interviewer_for_app4)
        self.assertEqual(interviewer3, interviewer_for_app3)

        self.assertTrue(application1 in interviewer1.interviews.all())
        self.assertTrue(application5 in interviewer1.interviews.all())
        self.assertTrue(application2 in interviewer2.interviews.all())
        self.assertTrue(application4 in interviewer2.interviews.all())
        self.assertTrue(application3 in interviewer3.interviews.all())
