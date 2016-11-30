from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Invitation
from .consumers import InvitationConsumer


@receiver(post_save, sender=Invitation)
def send_message_to_group(sender, instance, **kwargs):
    text = "New invitation was created."
    InvitationConsumer.group_send(name='Invitation', text=text)
    # Group("invitations").send({"message": message,
    #                            "competitor_id": instance.competitor.id})
