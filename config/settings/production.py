from .common import *  # noqa

EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='anymail.backends.mailgun.MailgunBackend')

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

DJANGO_DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL')


ANYMAIL = {
    "MAILGUN_API_KEY": env('MAILGUN_API_KEY'),
}

# Token that raspberry pi sends us for mac address checkins.
CHECKIN_TOKEN = env('CHECKIN_TOKEN')

GITHUB_OATH_TOKEN = env('GITHUB_OATH_TOKEN')

DJOSER['DOMAIN'] = env('DJOSER_DOMAIN')
DJOSER['SITE_NAME'] = env('DJOSER_SITE_NAME')
