import json

from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Invitation
from .consumers import InvitationConsumer


@receiver(post_save, sender=Invitation)
def send_message_to_group(sender, instance, **kwargs):
    # TODO: Broadcast only when instance is created?
    msg = "New invitation was created."
    leader_name = instance.team.get_leader().full_name
    competitor_id = instance.competitor.id

    data = {
        'message': msg,
        'leader': leader_name,
        'competitor_id': competitor_id
    }

    InvitationConsumer.group_send(name='Invitation', text=json.dumps(data))
