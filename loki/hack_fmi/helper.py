from datetime import datetime, timedelta
from django.conf import settings

from post_office import mail


def send_team_delete_email(team):
    members = list(team.members.all())
    user_emails = [member.email for member in members]
    sender = settings.EMAIL_HOST_USER
    mail.send(
        user_emails,
        sender,
        template='delete_team',
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
