import jwt
import json


from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import AuthenticationFailed
from channels.generic.websockets import BaseConsumer
from channels import Group

from .helper import authenticate, close_connection


class InvitationConsumer(BaseConsumer):

    USER_ADDED_TO_GROUP_MESSAGE = json.dumps({'message': 'User added to group.'})

    method_mapping = {
        "websocket.receive": "receive",
    }

    def receive(self, message, **kwargs):
        # auth
        msg = message.get('text')
        try:
            """
            Invalid message was provided.
            Valid json with key `token` is expected.
            """
            payload = json.loads(msg)
            token = payload.get('token')
            assert(token)

            user_id = authenticate(token)
            assert(user_id)

        except (ValueError, AssertionError, ObjectDoesNotExist, AuthenticationFailed,
                jwt.ExpiredSignature, jwt.DecodeError):
            return close_connection(message)

        self.add_to_group(message, user_id)

    def add_to_group(self, message, user_id):
        # Add them to the right group
        group_name = settings.INVITATION_GROUP_NAME.format(id=user_id)
        Group(group_name).add(message.reply_channel)
        message.reply_channel.send({'text': self.USER_ADDED_TO_GROUP_MESSAGE})
