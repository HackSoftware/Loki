from loki import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from post_office import mail

from ..models import Invitation


@receiver(post_save, sender=Invitation)
def send_invitation(**kwargs):

    competitor = kwargs.get('instance').competitor

    sender = settings.DEFAULT_FROM_EMAIL

    mail.send(
        competitor.email,
        sender,
        template='hackfmi_team_invite',
    )
