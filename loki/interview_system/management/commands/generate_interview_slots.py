from django.core.management.base import BaseCommand

from loki.interview_system.helpers.interviews import (GenerateInterviews,
                                                      GenerateInterviewSlots)
from loki.applications.models import ApplicationInfo


class Command(BaseCommand):
    help = "Generate free interview slots"

    def handle(self, **options):

        interview_length = 20
        break_between_interviews = 10

        interview_slots_generator = GenerateInterviewSlots(
            interview_length, break_between_interviews)

        interview_slots_generator.generate_interview_slots()
        generated_slots = interview_slots_generator.get_generated_slots()

        courses_to_interview = ApplicationInfo.objects.get_open_for_interview()

        for info in courses_to_interview:
            interview_generator = GenerateInterviews(application_info=info)
            interview_generator.generate_interviews()

            generated_interviews = interview_generator.get_generated_interviews_count()
            application_without_interviews = interview_generator.get_applications_without_interviews()

            print(str(generated_interviews) + " interviews were generated")
            print("Applications without interviews " + str(application_without_interviews))
