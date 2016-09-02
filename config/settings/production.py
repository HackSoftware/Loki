from .common import *  # noqa

"""
Secret configuration

- See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
- Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
"""

SECRET_KEY = env('DJANGO_SECRET_KEY')

"""
Site configuration

- Hosts/domain names that are valid for this site
- See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
- Custom Admin URL, use {% url 'admin:index' %}
"""
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
ADMIN_URL = env('DJANGO_ADMIN_URL')

DATABASES['default'] = env.db('DATABASE_URL')

BROKER_URL = env('BROKER_URL')

GRADER_ADDRESS = env('GRADER_ADDRESS')
GRADER_API_KEY = env('GRADER_API_KEY')
GRADER_API_SECRETCHECKIN_TOKEN = env('GRADER_API_SECRET')

# Email settings
EMAIL_BACKEND = 'anymail.backends.mailgun.MailgunBackend'

DJANGO_DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL', default="HackBulgaria <team@hackbulgaria.com>")

ANYMAIL = {
    "SENDGRID_MERGE_FIELD_FORMAT": "-{}-",
    "SENDGRID_API_KEY": env('SENDGRID_API_KEY'),
}

SENDGRID_TEMPLATES = {
    "user_registered": env('USER_REGISTER_TEMPLATE_ID'),
    "password_reset": env('PASSWORD_RESET_TEMPLATE_ID'),
    "hackfmi_team_deleted": env('HACKFMI_TEAM_DELETED_TEMPLATE_ID'),
}

# Token that raspberry pi sends us for mac address checkins.
CHECKIN_TOKEN = env('CHECKIN_TOKEN')
GITHUB_OATH_TOKEN = env('GITHUB_OATH_TOKEN')

DJOSER['DOMAIN'] = env('DJOSER_DOMAIN')
DJOSER['SITE_NAME'] = env('DJOSER_SITE_NAME')
