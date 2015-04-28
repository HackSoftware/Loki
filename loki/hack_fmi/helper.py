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
