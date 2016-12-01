import json
from channels import Group

from django.conf import settings
from channels.generic.websockets import BaseConsumer


from .helper import authenticate, close_connection


class InvitationConsumer(BaseConsumer):

    method_mapping = {
        "websocket.connect": "connect",
        "websocket.disconnect": "disconnect",
        "websocket.receive": "receive",
    }

    def connect(self, message, **kwargs):
        print("connect")

    def receive(self, message, **kwargs):
        # auth
        token = json.loads(message.get('text'))['token']
        user_id = authenticate(token)
        print("userid", user_id)
        if not user_id:
            close_connection(message)
        print("authenticated")
        # add in group
        self.add_to_group(message, user_id)

    def add_to_group(self, message, user_id):
        # Add them to the right group
        group_name = settings.INVITATION_GROUP_NAME.format(id=user_id)
        Group(group_name).add(message.reply_channel)
        print(group_name + " group created")

    def disconnect(self, message, **kwargs):
        print("disconnect")
