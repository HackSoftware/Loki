import jwt
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import AuthenticationFailed

from channels import Group
from channels.generic.websockets import WebsocketConsumer
from channels.handler import AsgiRequest
# from rest_framework_jwt.mixins import jwt_get_user_id_from_payload
from rest_framework_jwt.utils import jwt_decode_handler


def _authenticate(token):
    # Checks whether the token is valid
    try:
        payload = jwt_decode_handler(token)
    except jwt.ExpiredSignature:
        msg = 'Signature has expired.'
        raise AuthenticationFailed(msg)
    except jwt.DecodeError:
        msg = 'Error decoding signature.'
        raise AuthenticationFailed(msg)

    user = _authenticate_credentials(payload)

    return user


def _authenticate_credentials(payload):
    # Get the BaseUser with request token

    try:
        user_id = payload.get('user_id')

        if user_id:
            user = get_user_model().objects.get(pk=user_id, is_active=True)
        else:
            msg = 'Invalid payload'
            raise AuthenticationFailed(msg)
    except ObjectDoesNotExist:
        msg = 'Invalid signature'
        raise AuthenticationFailed(msg)

    return user


def _close_reply_channel(message):
    message.reply_channel.send({'close': True})


class InvitationServer(WebsocketConsumer):

    def connect(self, message, **kwargs):
        # The connection is opened on /login
        try:
            if "method" not in message.content:
                message.content['method'] = "FAKE"

            request = AsgiRequest(message)
        except Exception as e:
            raise ValueError("Cannot parse HTTP message - are you sure this is a HTTP consumer? %s" % e)

        # token = request.META.get("token", None)
        token = request.GET.get("token", None)
        if token is None:
            _close_reply_channel(message)
            raise ValueError("Missing token request parameter. Closing channel.")

        user = _authenticate(token)

        message.token = token
        message.user = user

        Group("invitations").add(message.reply_channel)

    def disconnect(self, message, **kwargs):
        Group("invitations").discard(message.reply_channel)
