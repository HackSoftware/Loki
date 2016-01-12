import re

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def validate_mac(mac):
    # RegexValidator uses re.search, which has no use for us
    regex = re.compile(r'^([0-9a-f]{2}[:]){5}([0-9a-f]{2})$', re.IGNORECASE)
    if not re.match(regex, mac):
        raise ValidationError('{} is not a valid mac address'.format(mac), 'invalid_mac_address')


def validate_url(url):
    # Check if url is valid
    val = URLValidator()
    try:
        val(url)
    except ValidationError:
        raise ValidationError('{} is not a valid URL'.format(url))

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
