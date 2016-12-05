import jwt
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.utils import jwt_decode_handler

from loki.emails.services import send_template_email

from loki.base_app.models import BaseUser


def send_team_delete_email(team):
    for member in team.members.all():
        context = {
            'full_name': member.full_name,
            'team_name': team.name
        }

        send_template_email(
            member.email,
            settings.EMAIL_TEMPLATES['hackfmi_team_deleted'],
            context
        )


def send_invitation(invitation):
    receiver = invitation.competitor.email
    template_id = settings.EMAIL_TEMPLATES['send_invitation']
    context = {
        "receiver_full_name": BaseUser.objects.get(email=receiver).full_name,
        "leader_name": invitation.team.get_leader().full_name,
        "team_name": invitation.team.name,
    }
    send_template_email(receiver, template_id, context)


def date_increase(days):
    new_date = get_date_with_timedelta(days=days)
    result = new_date.strftime("%Y-%m-%d")
    return result


def date_decrease(days):
    new_date = get_date_with_timedelta(days=-days)
    result = new_date.strftime("%Y-%m-%d")
    return result


def get_object_variable_or_none(queryset, variable):
    if not queryset.first():
        return None
    return queryset.values(variable)[0][variable]


def get_date_with_timedelta(*, days):
    current_moment = timezone.now()
    return current_moment + timedelta(days=days)


def authenticate(token):
    # Checks whether the token is valid
    try:
        payload = jwt_decode_handler(token)
    except jwt.ExpiredSignature:
        msg = 'Signature has expired.'
        raise AuthenticationFailed(msg)
    except jwt.DecodeError:
        msg = 'Error decoding signature.'
        raise AuthenticationFailed(msg)
    user_id = authenticate_credentials(payload)

    return user_id


def authenticate_credentials(payload):
    # Get the BaseUser with request token

    try:
        user_id = payload.get('user_id')

        if user_id:
            get_user_model().objects.get(pk=user_id, is_active=True)
        else:
            msg = 'Invalid payload'
            raise AuthenticationFailed(msg)
    except ObjectDoesNotExist:
        msg = 'Invalid signature'
        raise AuthenticationFailed(msg)

    return user_id


def close_connection(message):
    message.reply_channel.send({'close': True})
