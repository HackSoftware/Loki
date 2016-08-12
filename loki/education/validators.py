import re

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_phone(phone_number):
    phone_pattern = "^(\+|)[0-9\s]+$"
    if not re.search(phone_pattern, phone_number):
        raise ValidationError("Невалиден телефонен номер")

def validate_mac(mac):
    # RegexValidator uses re.search, which has no use for us
    regex = re.compile(r'^([0-9a-f]{2}[:]){5}([0-9a-f]{2})$', re.IGNORECASE)
    if not re.match(regex, mac):
        raise ValidationError(_('{} is not a valid mac address'.format(mac)),
                                'invalid_mac_address')

def validate_github_account(github_account):
    github_pattern = "^http(|s):\/\/github.com\/[^\/]+$"
    if not re.search(github_pattern, github_account):
        raise ValidationError("Невалиден Github акаунт")

def validate_url(url):
    # Check if url is valid
    val = URLValidator()
    try:
        val(url)
    except ValidationError:
        raise ValidationError('{} is not a valid URL'.format(url))


def validate_github_solution_url(url):
    validate_url(url)

    github_domain = "github.com"
    splitted_url = url.split("/")
    file_name = splitted_url[-1]

    # Check if the url has github domain and ends with fail extension
    if github_domain not in splitted_url:
        raise ValidationError('{} is not a valid URL'.format(url))
    if "." not in file_name:
        raise ValidationError('{} is not a valid URL'.format(url))
    elif len(file_name) <= file_name.index(".") + 1:
        raise ValidationError('{} is not a valid URL'.format(url))


def validate_github_project_url(url):
    validate_url(url)

    github_domain = "github.com"
    splitted_url = url.split("/")

    # Check if the url has github domain and ends with fail extension
    if github_domain not in splitted_url:
        raise ValidationError('{} is not a valid URL'.format(url))
