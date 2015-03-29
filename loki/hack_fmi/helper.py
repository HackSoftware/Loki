from django.core.mail import send_mail
from django.template.loader import render_to_string

import random


def get_random_code(len):
    return ''.join(str(random.randint(0, 9)) for _ in range(len))


def send_registration_mail(user):
    message = render_to_string("mails/registration.html", {
        'user': user
    })
    send_mail(
        'HackFMI регистрация',
        message,
        'from@example.com',
        (user.email,)
    )
