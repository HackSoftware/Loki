from __future__ import absolute_import

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from anymail.exceptions import AnymailError
from celery import shared_task


@shared_task(bind=True, max_retries=settings.CELERY_TASK_MAX_RETRIES)
def send_mail(self, recipient, template_id, context, **kwargs):
    # Subject and body can't be empty. Empty string or space return index out of range error
    message = EmailMultiAlternatives(
        subject="-",
        body="-",
        from_email=settings.DJANGO_DEFAULT_FROM_EMAIL,
        to=[recipient]
    )

    # Otherwise SendGrid does not sent html
    message.attach_alternative(" ", "text/html")

    message.template_id = template_id
    message.merge_data = {
        recipient: context,
    }

    try:
        message.send()
    except AnymailError as e:
        self.retry(e)
