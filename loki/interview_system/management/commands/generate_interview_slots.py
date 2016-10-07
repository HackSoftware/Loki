from django.core.management.base import BaseCommand

from loki.interview_system.helpers.interviews import (GenerateInterviews,
                                                      GenerateInterviewSlots)
from loki.applications.models import ApplicationInfo


class Command(BaseCommand):
    help = "Generate free interview slots"

    def handle(self, **options):

        print("Start generating interviews...\n")
        interview_length = 20
        break_between_interviews = 10

        interview_slots_generator = GenerateInterviewSlots(
            interview_length, break_between_interviews)

        interview_slots_generator.generate_interview_slots()
        interview_slots_generator.get_generated_slots()

        courses_to_interview = ApplicationInfo.objects.get_open_for_interview()

        if len(courses_to_interview) == 0:
            print('There are no open for interview courses!\n')
            print('No interviews will be generated.')
        for info in courses_to_interview:
            print("Generate interviews for {0}".format(info.course.course.name))
            interview_generator = GenerateInterviews(application_info=info)
            interview_generator.generate_interviews()

            generated_interviews = interview_generator.get_generated_interviews_count()
            application_without_interviews = interview_generator.get_applications_without_interviews()
            free_interview_slots = interview_generator.get_free_interview_slots()
            print('Generated interviews: {0}'.format(generated_interviews))
            print('Applications without interviews: {0} '.format(
                   application_without_interviews))
            print('All free interview slots: {0}'.format(free_interview_slots))
