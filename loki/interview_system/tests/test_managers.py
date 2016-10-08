import datetime
import factory
from test_plus.test import TestCase
from ..models import InterviewerFreeTime, Interview
from loki.seed.factories import (ApplicationFactory, ApplicationInfoFactory,
                                 CourseFactory, CourseDescriptionFactory,
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

    def test_counting_interview_slots_for_app_info_without_applications(self):
        course1, course2 = factory.build_batch(size=2, klass=CourseFactory)
        cd1 = CourseDescriptionFactory(course=course1)
        cd2 = CourseDescriptionFactory(course=course2)
        app_info1 = ApplicationInfoFactory(course=cd1)
        app_info2 = ApplicationInfoFactory(course=cd2)

        interviewer1 = InterviewerFactory()
        interviewer1.courses_to_interview.add(app_info1)
        interviewer2 = InterviewerFactory()
        interviewer2.courses_to_interview.add(app_info2)

        free_time1 = InterviewerFreeTime.objects.create(interviewer=interviewer1,
                                                        date=datetime.datetime.now().date(),
                                                        start_time='11:00',
                                                        end_time='14:00')
        free_time2 = InterviewerFreeTime.objects.create(interviewer=interviewer1,
                                                        date=datetime.datetime.now().date(),
                                                        start_time='10:00',
                                                        end_time='14:00')

        Interview.objects.create(interviewer=interviewer2,
                                 date=datetime.datetime.now().date(),
                                 start_time='12:00',
                                 end_time='12:30',
                                 interviewer_time_slot=free_time2)

        Interview.objects.create(interviewer=interviewer2,
                                 date=datetime.datetime.now().date(),
                                 start_time='12:00',
                                 end_time='12:30',
                                 interviewer_time_slot=free_time2)

        interview = Interview.objects.create(interviewer=interviewer1,
                                             date=datetime.datetime.now().date(),
                                             start_time='11:00',
                                             end_time='11:30',
                                             interviewer_time_slot=free_time1)

        Interview.objects.create(interviewer=interviewer1,
                                 date=datetime.datetime.now().date(),
                                 start_time='12:00',
                                 end_time='12:30',
                                 interviewer_time_slot=free_time1)

        self.assertEquals(2, Interview.objects.free_slots_for(app_info1).count())
        self.assertEquals(2, Interview.objects.free_slots_for(app_info2).count())
        self.assertEquals(4, Interview.objects.get_free_slots().count())

        application = ApplicationFactory(application_info=app_info1)
        interview.application = application
        interview.save()

        self.assertEquals(1, Interview.objects.free_slots_for(app_info1).count())
        self.assertEquals(2, Interview.objects.free_slots_for(app_info2).count())
        self.assertEquals(3, Interview.objects.get_free_slots().count())
