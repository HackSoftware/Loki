from .tasks import send_mail


def send_template_email(recipient, template_id, context):
    return send_mail.delay(recipient, template_id, context)
