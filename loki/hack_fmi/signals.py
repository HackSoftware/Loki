import json
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from channels import Group

from .models import Invitation


@receiver(post_save, sender=Invitation)
def send_message_to_group(sender, instance, **kwargs):
    text = {"message": "New invitation was created.",
            "competitor_id": instance.competitor.id
            }
    group_name = settings.INVITATION_GROUP_NAME.format(id=instance.competitor.id)
    Group(group_name).send({"text": json.dumps(text)})
