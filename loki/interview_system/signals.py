from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Interview


@receiver(post_delete, sender=Interview)
def delete_has_interview_date_in_application(sender, instance, **kwargs):
    if instance.application:
        instance.application.has_interview_date = False
        instance.application.save()
