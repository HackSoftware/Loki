from django.core.management.base import BaseCommand
from django.conf import settings

from loki.interview_system.models import Interview
from loki.emails.services import send_template_email


class Command(BaseCommand):
    help = "Send emails to applicants"

    def handle(self, **options):
        interviews = Interview.objects.with_application().without_received_email()
        for interview in interviews:
            application = interview.application
            user = application.user

            context = {
                'full_name': user.full_name,
                'course_name': application.application_info.course.course.name,
                'start_time': str(interview.start_time),
                'date': str(interview.date)
            }

            # TODO: Add ability to set custom template from the model
            email_template = settings.EMAIL_TEMPLATES['interview_confirmation']
            send_template_email(user.email, email_template, context)
            import ipdb; ipdb.set_trace()

            interview.has_received_email = True
            interview.save()
