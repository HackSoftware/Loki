from datetime import datetime, timedelta
from django.conf import settings

from loki.emails.services import send_template_email


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
