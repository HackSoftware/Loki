from .common import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATE_DEBUG = env.bool('DJANGO_TEMPLATE_DEBUG', default=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='8n)k%#*mt*s3gwtfs@_c!107m91g%bfsch(*c2(%7z3#9csd4!')

EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

ALLOWED_HOSTS = []
