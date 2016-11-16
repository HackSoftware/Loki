from django.conf import settings
# from django.dispatch import receiver
# from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
# from ..models import Invitation


# @receiver(post_save, sender=Invitation)
def send_invitation(instance, **kwargs):
    competitor_email = instance.competitor.email
    subject = "Invitation for hackFMI membership"
    body = """Greetings {}!! You have been invited to join the {} team in the {}.
              Please make up your choice and let your teamleader know your decision :)
           """.format(instance.competitor.first_name,
                      instance.team.name,
                      instance.team.season.name)

    msg = EmailMultiAlternatives(subject=subject,
                                 body=body,
                                 from_email=settings.DJANGO_DEFAULT_FROM_EMAIL,
                                 to=[competitor_email])

    msg.send()
