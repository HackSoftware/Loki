from django.db.models.signals import post_save
from django.dispatch import receiver

from chnnels import Group
from .models import Invitation


# @receiver(post_save, sender=Invitation)
# def send_message_to_group(sender, instance, **kwargs):
#     print("erfre")
#     Group("invitations").send({"text": "tuk sum"})
