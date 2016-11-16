from datetime import datetime, timedelta
from django.conf import settings

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
    link = ''
    context = {
        "receiver_full_name": BaseUser.objects.get(email=receiver).full_name,
        "leader_name": invitation.team.get_leader().full_name,
        "team_name": invitation.team.name,
        "redirect_link": link
    }
    send_template_email(receiver, template_id, context)


def date_increase(days):
    old_date = datetime.now()
    new_date = old_date + timedelta(days=days)
    result = new_date.strftime("%Y-%m-%d")
    return result


def date_decrease(days):
    old_date = datetime.now()
    new_date = old_date - timedelta(days=days)
    result = new_date.strftime("%Y-%m-%d")
    return result
