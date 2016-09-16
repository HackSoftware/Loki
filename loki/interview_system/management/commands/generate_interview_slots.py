from django.core.management.base import BaseCommand

from loki.interview_system.helpers.interviews import GenerateInterviews, GenerateInterviewSlots


class Command(BaseCommand):
    help = "Generate free interview slots"

    def handle(self, **options):

        interview_length = 20
        break_between_interviews = 10

        interview_slots_generator = GenerateInterviewSlots(
            interview_length, break_between_interviews)

        interview_slots_generator.generate_interview_slots()
        generated_slots = interview_slots_generator.get_generated_slots()


        interview_generator = GenerateInterviews()
        import ipdb; ipdb.set_trace()
        interview_generator.generate_interviews()

        generated_interviews = interview_generator.get_generated_interviews_count()

        print(str(generated_interviews) + " interviews were generated")
