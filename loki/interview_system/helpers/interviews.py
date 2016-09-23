from datetime import datetime, timedelta
from loki.applications.models import Application

from ..models import InterviewerFreeTime, Interview
from .groups_generator import cycle_groups

class GenerateInterviewSlots:

    def __init__(self, interview_time_length, break_time):
        self.interview_time_length = interview_time_length
        self.break_time = break_time
        self.__slots_generated = 0

    def __inc_slots_generated(self):
        self.__slots_generated += 1

    def __calculate_diff_in_time(self, start_time, end_time):
        start_delta = timedelta(
            hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second)
        end_delta = timedelta(
            hours=end_time.hour, minutes=end_time.minute, seconds=end_time.second)
        return (end_delta - start_delta).seconds / 60

    def generate_interview_slots(self):
        teacher_time_slots = InterviewerFreeTime.objects.all().order_by('date')

        for slot in teacher_time_slots:
            # Check if slots are already generated for that time_slot
            # (by a previous invocation of manage.py generate_slots)
            if slot.has_generated_slots():
                continue

            # summarized free time of the interviewer
            free_time = self.__calculate_diff_in_time(slot.start_time, slot.end_time)
            # starting time of the first interview
            interview_start_time = slot.start_time

            while free_time >= self.interview_time_length:
                if slot.buffer_time:
                    Interview.objects.create(
                        interviewer=slot.interviewer,
                        interviewer_time_slot=slot,
                        date=slot.date,
                        start_time=interview_start_time,
                        buffer_time=True)
                else:
                    Interview.objects.create(
                        interviewer=slot.interviewer,
                        interviewer_time_slot=slot,
                        date=slot.date,
                        start_time=interview_start_time,
                        buffer_time=False)

                self.__inc_slots_generated()

                # Decrease the free time and change the starting time of the next interview
                free_time -= (self.interview_time_length + self.break_time)
                next_interview_date_and_time = datetime.combine(
                        slot.date, interview_start_time) + timedelta(
                        minutes=(self.interview_time_length + self.break_time))
                interview_start_time = next_interview_date_and_time.time()

    def get_generated_slots(self):
        return self.__slots_generated


class GenerateInterviews:

    def __init__(self):
        self.__generated_interviews = 0

    def __inc_generated_interviews(self):
        self.__generated_interviews += 1

    def generate_interviews(self):
        applications = iter(Application.objects.without_interviews())
        free_interview_slots = cycle_groups(Interview.objects.get_free_slots())
        today = datetime.now()

        for slot in free_interview_slots:
            if slot.interviewer_time_slot.date < datetime.date(today):
                continue

            try:
                application = next(applications)
            except StopIteration:
                break

            interviewer_courses = slot.interviewer.courses_to_interview
            course = application.course

            slot.application = application
            slot.save()

            application.has_interview_date = True
            application.save()

            self.__inc_generated_interviews()

    def get_applications_without_interviews(self):
        return Application.objects.without_interviews().count()

    def get_generated_interviews_count(self):
        return self.__generated_interviews
