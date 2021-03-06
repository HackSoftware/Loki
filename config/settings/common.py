# flake8: noqa
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from easy_thumbnails.conf import Settings as thumbnail_settings

from datetime import timedelta
from celery.schedules import crontab

"""
Django settings for loki project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import environ

env = environ.Env()


ROOT_DIR = environ.Path(__file__) - 3  # (loki/loki/settings/common.py - 3 = loki/)
APPS_DIR = ROOT_DIR.path('loki')

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',
    'ckeditor',
    'adminsortable2',
    'django_resized',
    'import_export',
    'djcelery',
    'crispy_forms',
    'anymail',
    'easy_thumbnails',
    'image_cropping',
    'channels',
    'captcha',
    'raven.contrib.django.raven_compat',
    'loki.hack_fmi.apps.HackFMIConfig',
    'loki.base_app.apps.BaseAppConfig',
    'loki.education.apps.EducationConfig',
    'loki.status.apps.StatusConfig',
    'loki.website.apps.WebsiteConfig',
    'loki.applications.apps.ApplicationConfig',
    'loki.emails.apps.EmailsConfig',
    'loki.interview_system.apps.InterviewSystemConfig',
)

MIDDLEWARE_CLASSES = (
    # Used for sentry client setup. For more info check the docs:
    # https://docs.sentry.io/clients/python/integrations/django/
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

MIGRATION_MODULES = {
    'sites': 'loki.contrib.sites.migrations'
}

DEBUG = env.bool('DJANGO_DEBUG', False)


# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'


# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------

# Custom user app defaults
AUTH_USER_MODEL = 'base_app.BaseUser'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'bg'

USE_I18N = True

USE_L10N = True

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (('bg', 'Bulgarian'),)

TIME_ZONE = env('TIME_ZONE', default='Europe/Sofia')

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'UPLOADED_FILES_USE_URL': False,
}

# JWT Authorization
JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    # Set expiration time to 1 week.
    'JWT_EXPIRATION_DELTA': timedelta(seconds=604800),
}

# # CELERY
# INSTALLED_APPS += ('loki.celery.CeleryConfig',
#                    'django.contrib.gis',)

# if you are not using the django database broker (e.g. rabbitmq, redis, memcached), you can remove the next line.
BROKER_URL = env('BROKER_URL', default='amqp://guest:guest@localhost//')
# Configure celery to use the django-celery backend
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# Configure celery to use json instead of pickle
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

"""
   Celery time limits
   Default soft limit is 1 minute
   Default hard limit is 2 minutes
"""
CELERYD_TASK_SOFT_TIME_LIMIT = env('CELERYD_TASK_SOFT_TIME_LIMIT', default=60)
CELERYD_TASK_TIME_LIMIT = env('CELERYD_TASK_TIME_LIMIT', default=60 + 60)
CELERY_TASK_MAX_RETRIES = env('CELERY_TASK_MAX_RERIES', default=101)

# grader api
GRADER_GRADE_PATH = "/grade"
GRADER_CHECK_PATH = "/check_result/{buildID}/"
GRADER_GET_NONCE_PATH = "/nonce"
GRADER_ADDRESS = env('GRADER_ADDRESS', default='https://grader.hackbulgaria.com')
GRADER_API_KEY = env('GRADER_API_KEY', default='')
GRADER_API_SECRET = env('GRADER_API_SECRET', default='')

POLLING_SLEEP_TIME = env.int('POLLING_SLEEP_TIME', default=1)  # seconds

CELERY_TIMEZONE = 'Europe/Sofia'
CELERYBEAT_SCHEDULE = {
    'retest-solutions-on-test-change': {
        'task': 'loki.education.tasks.check_for_retests',
        'schedule': timedelta(seconds=60),
    },
    'calculate-presence-every-day': {
        'task': 'loki.education.tasks.execute_calculate_presense_command',
        'schedule': crontab(minute=45, hour=19, day_of_week='mon-fri'),
    }
}

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db('DATABASE_URL', default='postgres:///loki'),
}

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

MEDIA_ROOT = str(ROOT_DIR('media'))

MEDIA_URL = '/media/'

CKEDITOR_UPLOAD_PATH = "uploads/"

# TODO: Just for the begining
CORS_ORIGIN_ALLOW_ALL = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}

# THUMBNAILS CONFIGURATION
# ------------------------------------------------------------------------------

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DJANGO_DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL', default="HackBulgaria <team@hackbulgaria.com>")

TEMPLATE_CONTEXT_PROCESSORS = TCP + [
    'django.core.context_processors.request',
    'loki.applications.processors.apply_active_courses',
]

# Token that raspberry pi sends us for mac address checkins.
CHECKIN_TOKEN = env('CHECKIN_TOKEN', default="")

GITHUB_OATH_TOKEN = env('GITHUB_OATH_TOKEN', default="")

templates = {
    "user_registered": lambda **env_kwargs: env('USER_REGISTER_TEMPLATE_ID', **env_kwargs),
    "password_reset": lambda **env_kwargs: env('PASSWORD_RESET_TEMPLATE_ID', **env_kwargs),
    "application_completed_default": lambda **env_kwargs: env('APPLICATION_COMPLETED_DEFAULT', **env_kwargs),
    "hackfmi_team_deleted": lambda **env_kwargs: env('HACKFMI_TEAM_DELETED_TEMPLATE_ID', **env_kwargs),
    "interview_confirmation": lambda **env_kwargs: env('CONFIRM_INTERVIEW', **env_kwargs),
    "send_invitation": lambda **env_kwargs: env('SEND_INVITATION', **env_kwargs),
    "hackfmi_register": lambda **env_kwargs: env('HACKFMI_REGISTER', **env_kwargs)
}

# Get all email templates from the env with default value ""
EMAIL_TEMPLATES = {
    key: f(default="")
    for key, f in templates.items()
}

LOGIN_URL = 'website:login'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgiref.inmemory.ChannelLayer",
        "ROUTING": "config.routing.channel_routing",
    },
}

INVITATION_GROUP_NAME = "Invitations-{id}"

# captcha settings
NOCAPTCHA = True
RECAPTCHA_PUBLIC_KEY = env('RECAPTCHA_PUBLIC_KEY', default="")
RECAPTCHA_PRIVATE_KEY = env('RECAPTCHA_PRIVATE_KEY', default="")
RECAPTCHA_USE_SSL = True
