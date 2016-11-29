import uuid

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from operator import itemgetter
from fuzzywuzzy import fuzz

from loki.emails.services import send_template_email

from .helper import get_activation_url
from .models import (Subject, School, Academy,
                     BaseUserRegisterToken, BaseUserPasswordResetToken)


FILTER_UNDER_TRESHOLD = 30
EXCLUDE_FIELDS = ('pk', 'faculty_pk', 'subject_pk',
                  'total_score')


def get_possible_universities():
    subjects = Subject.objects.all()
    possible = [{
        'pk': s.faculty.university.pk,
        'subject_pk': s.pk,
        'faculty_pk': s.faculty.pk,
        'subject': s.name,
        'faculty': s.faculty.name,
        'faculty_abbreviation': s.faculty.abbreviation or "",
        'educationplace': s.faculty.university.name,
        'city': s.faculty.university.city.name,
        'total_score': 0
    } for s in subjects]

    return possible


def get_possible_schools():
    schools = School.objects.all()
    possible = [
        {'pk': s.pk,
         'educationplace': s.name,
         'city': s.city.name,
         'total_score': 0} for s in schools]

    return possible


def get_possible_academies():
    academies = Academy.objects.all()
    possible = [
        {'pk': a.pk,
         'educationplace': a.name,
         'city': a.city.name,
         'total_score': 0} for a in academies]

    return possible


def fuzzy_search_education_place(words):
    universities = get_possible_universities()
    # schools = get_possible_schools()
    schools = []
    academies = get_possible_academies()

    everything = universities + schools + academies

    for word in set(words):
        for obj in everything:
            s = 0
            c = 0

            for field in obj:
                if field in EXCLUDE_FIELDS:
                    continue

                ratio = fuzz.ratio(word.lower(), obj[field].lower())

                s += ratio
                c += 1

            obj['total_score'] += s / c

    flatten = sorted(everything, key=itemgetter('total_score'), reverse=True)

    return list(filter(lambda r: r['total_score'] >= FILTER_UNDER_TRESHOLD, flatten))[:5]


def send_activation_mail(request, user):
    to_email = user.email

    BaseUserRegisterToken.objects.filter(user=user).delete()

    # TODO: check if it exsists
    user_token = BaseUserRegisterToken.objects.create(
        user=user,
        token=uuid.uuid4())

    context = {
        'protocol': request.is_secure() and 'https' or 'http',
        'domain': Site.objects.get_current().domain,
        'url': get_activation_url(user_token.token, request.GET.get('origin', None)),
        'full_name': user.full_name
    }
    if request.GET.get('origin') == "hackfmi":
        template_id = settings.EMAIL_TEMPLATES['hackfmi_register']
    else:
        template_id = settings.EMAIL_TEMPLATES['user_registered']

    send_template_email(to_email, template_id, context)


def send_forgotten_password_email(request, user):
    to_email = user.email

    BaseUserPasswordResetToken.objects.filter(user=user).delete()

    # TODO: check if it exsists
    user_token = BaseUserPasswordResetToken.objects.create(
        user=user,
        token=uuid.uuid4())

    context = {
        'protocol': request.is_secure() and 'https' or 'http',
        'domain': Site.objects.get_current().domain,
        'url': reverse("base_app:user_password_reset", kwargs={"token": user_token.token}),
        'full_name': user.full_name
    }

    template_id = settings.EMAIL_TEMPLATES['password_reset']

    send_template_email(to_email, template_id, context)
