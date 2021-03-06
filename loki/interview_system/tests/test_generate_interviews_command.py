import factory
from datetime import datetime, timedelta
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
                                           date=datetime.now().date(),
                                           start_time='11:00',
                                           end_time='14:00')

        self.assertEqual(0, Interview.objects.count())
        self.assertFalse(application.has_interview_date)
        self.assertEquals(1, Application.objects.without_interviews_for(app_info).count())

        call_command('generate_interview_slots')

        self.assertEqual(1, Interview.objects.filter(application__isnull=False).count())
        self.assertEquals(0, Application.objects.without_interviews_for(app_info).count())

    def test_interviews_are_generated_correctly_if_new_application_is_added_after_generation(self):
        app_info = ApplicationInfoFactory()
        ApplicationFactory(application_info=app_info)
        interviewer = InterviewerFactory()
        interviewer.courses_to_interview.add(app_info)

        InterviewerFreeTime.objects.create(interviewer=interviewer,
                                           date=datetime.now().date(),
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
        interviewer1, interviewer2 = factory.build_batch(size=2,
                                                         klass=InterviewerFactory)

        interviewer1.courses_to_interview.add(app_info)
        interviewer2.courses_to_interview.add(app_info)

        InterviewerFreeTime.objects.create(interviewer=interviewer1,
                                           date=datetime.now().date(),
                                           start_time='11:00',
                                           end_time='14:00')

        InterviewerFreeTime.objects.create(interviewer=interviewer2,
                                           date=datetime.now().date(),
                                           start_time='12:00',
                                           end_time='15:00')

        self.assertEquals(3, Application.objects.without_interviews_for(app_info).count())

        call_command('generate_interview_slots')
        self.assertEquals(9, Interview.objects.free_slots_for(app_info).count())
        interviewer_for_app1 = Interview.objects.get(application=application1).interviewer
        interviewer_for_app2 = Interview.objects.get(application=application2).interviewer
        interviewer_for_app3 = Interview.objects.get(application=application3).interviewer
        self.assertNotEqual(interviewer_for_app1, interviewer_for_app2)
        self.assertEqual(interviewer_for_app1, interviewer_for_app3)
        self.assertEquals(0, Application.objects.without_interviews_for(app_info).count())

    def test_generate_interviews_for_different_courses_with_different_interviewers(self):
        course1, course2 = factory.build_batch(size=2, klass=CourseFactory)
        cd1 = CourseDescriptionFactory(course=course1)
        cd2 = CourseDescriptionFactory(course=course2)
        app_info1 = ApplicationInfoFactory(course=cd1)
        app_info2 = ApplicationInfoFactory(course=cd2)

        application1 = ApplicationFactory(application_info=app_info1)
        application2 = ApplicationFactory(application_info=app_info2)
        application3 = ApplicationFactory(application_info=app_info1)
        application4 = ApplicationFactory(application_info=app_info2)
        application5 = ApplicationFactory(application_info=app_info1)
        interviewer1, interviewer2, interviewer3 = factory.build_batch(size=3,
                                                                       klass=InterviewerFactory)

        interviewer1.courses_to_interview.add(app_info1)
        interviewer2.courses_to_interview.add(app_info2)
        interviewer3.courses_to_interview.add(app_info1)

        InterviewerFreeTime.objects.create(interviewer=interviewer1,
                                           date=datetime.now().date(),
                                           start_time='11:00',
                                           end_time='14:00')
        InterviewerFreeTime.objects.create(interviewer=interviewer2,
                                           date=datetime.now().date(),
                                           start_time='12:00',
                                           end_time='15:00')
        InterviewerFreeTime.objects.create(interviewer=interviewer3,
                                           date=datetime.now().date(),
                                           start_time='13:00',
                                           end_time='15:00')

        self.assertEquals(3, Application.objects.without_interviews_for(app_info1).count())
        self.assertEquals(2, Application.objects.without_interviews_for(app_info2).count())
        self.assertEquals(5, Application.objects.without_interviews().count())

        call_command('generate_interview_slots')
        self.assertEquals(7, Interview.objects.free_slots_for(app_info1).count())
        self.assertEquals(4, Interview.objects.free_slots_for(app_info2).count())
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

    def test_not_generate_interview_for_past_days(self):
        app_info = ApplicationInfoFactory()
        interviewer1, interviewer2 = factory.build_batch(size=2,
                                                         klass=InterviewerFactory)

        interviewer1.courses_to_interview.add(app_info)
        interviewer2.courses_to_interview.add(app_info)

        InterviewerFreeTime.objects.create(interviewer=interviewer1,
                                           date=datetime.now().date() - timedelta(days=1),
                                           start_time='11:00',
                                           end_time='14:00')

        InterviewerFreeTime.objects.create(interviewer=interviewer2,
                                           date=datetime.now().date(),
                                           start_time='11:00',
                                           end_time='14:00')

        call_command('generate_interview_slots')
        self.assertEquals(6, Interview.objects.get_free_slots().count())

    def test_not_generate_interviews_when_have_not_enough_free_slots(self):
        app_info = ApplicationInfoFactory()
        interviewer = InterviewerFactory()
        interviewer.courses_to_interview.add(app_info)

        InterviewerFreeTime.objects.create(interviewer=interviewer,
                                           date=datetime.now().date(),
                                           start_time='11:00',
                                           end_time='12:00')

        ApplicationFactory(application_info=app_info)
        ApplicationFactory(application_info=app_info)
        ApplicationFactory(application_info=app_info)
        self.assertEquals(3, Application.objects.without_interviews_for(app_info).count())

        call_command('generate_interview_slots')
        self.assertEquals(3, Application.objects.without_interviews_for(app_info).count())
        self.assertEquals(2, Interview.objects.free_slots_for(app_info).count())

    def test_not_generate_interviews_when_have_not_enough_free_slots_for_app_info(self):
        course1, course2 = factory.build_batch(size=2, klass=CourseFactory)
        cd1 = CourseDescriptionFactory(course=course1)
        cd2 = CourseDescriptionFactory(course=course2)
        app_info1 = ApplicationInfoFactory(course=cd1)
        app_info2 = ApplicationInfoFactory(course=cd2)

        ApplicationFactory(application_info=app_info1)
        ApplicationFactory(application_info=app_info1)
        ApplicationFactory(application_info=app_info1)
        ApplicationFactory(application_info=app_info2)
        ApplicationFactory(application_info=app_info2)
        interviewer1, interviewer2 = factory.build_batch(size=2, klass=InterviewerFactory)

        interviewer1.courses_to_interview.add(app_info1)
        interviewer2.courses_to_interview.add(app_info2)

        InterviewerFreeTime.objects.create(interviewer=interviewer1,
                                           date=datetime.now().date(),
                                           start_time='11:00',
                                           end_time='12:00')
        InterviewerFreeTime.objects.create(interviewer=interviewer2,
                                           date=datetime.now().date(),
                                           start_time='12:00',
                                           end_time='15:00')

        self.assertEquals(3, Application.objects.without_interviews_for(app_info1).count())
        self.assertEquals(2, Application.objects.without_interviews_for(app_info2).count())

        call_command('generate_interview_slots')
        self.assertEquals(3, Application.objects.without_interviews_for(app_info1).count())
        self.assertEquals(2, Interview.objects.free_slots_for(app_info1).count())
        self.assertEquals(0, Application.objects.without_interviews_for(app_info2).count())
        self.assertEquals(4, Interview.objects.free_slots_for(app_info2).count())
