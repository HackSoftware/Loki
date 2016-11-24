from datetime import timedelta
from django.conf import settings
from django.utils import timezone
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
