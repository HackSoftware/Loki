from __future__ import absolute_import

from django.core.mail import EmailMessage

from celery import shared_task

from django.conf import settings


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def send_mail(self, recipient, template_id, context, **kwargs):
    message = EmailMessage(
        subject=" ",  # We get subject from sendgrid
        body=" ",  # We get the body from sendgrid
        to=recipient
    )

    message.template_id = template_id  # SendGrid id
    message.merge_data = {
        recipient: context,
    }

    message.send()
