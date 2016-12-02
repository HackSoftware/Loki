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
        msg = message.get('text')
        try:
            payload = json.loads(msg)
        except ValueError:
            """
            Invalid message was provided.
            Valid json with key `token` is expected.
            """
            return close_connection(message)
        token = payload.get('token')

        if token is None:
            return close_connection(message)

        # TODO: This uses the wrong jwt package.
        # user_id = authenticate(token)
        # if not user_id:
        #     return close_connection(message)

        # self.add_to_group(message, user_id)

    def add_to_group(self, message, user_id):
        # Add them to the right group
        group_name = settings.INVITATION_GROUP_NAME.format(id=user_id)
        Group(group_name).add(message.reply_channel)
        print(group_name + " group created")

    def disconnect(self, message, **kwargs):
        print("disconnect")
