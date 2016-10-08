from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from loki.interview_system.models import Interview
from loki.emails.services import send_template_email


class Command(BaseCommand):
    help = "Send emails to applicants"

    def handle(self, **options):
        interviews = Interview.objects.with_application().without_received_email()
        for interview in interviews:
            application = interview.application
            user = application.user
            confirm_url_kwargs = {"application": application.id,
                                  "interview_token": interview.uuid}
            context = {
                'protocol': 'http',
                'full_name': user.full_name,
                'course_name': application.application_info.course.course.name,
                'start_time': str(interview.start_time),
                'date': str(interview.date),
                'domain': Site.objects.get_current().domain,
                'confirm_url': reverse("interview_system:confirm_interview",
                                       kwargs=confirm_url_kwargs),
                'choose_url': reverse("interview_system:choose_interview",
                                      kwargs={"application": application.id,
                                              "interview_token": interview.uuid})
            }

            print('Sending to {} for application {}'.format(user.email, application))

            email_template = settings.EMAIL_TEMPLATES['interview_confirmation']
            send_template_email(user.email, email_template, context)

            interview.has_received_email = True
            interview.save()
