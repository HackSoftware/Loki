# flake8: noqa
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from easy_thumbnails.conf import Settings as thumbnail_settings

"""
Django settings for loki project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = (
    'easy_thumbnails',
    'image_cropping',
    'post_office',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
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

    'hack_fmi.apps.HackFMIConfig',
    'base_app',
    'hack_conf',
    'education',
    'status',
    'website',
    'applications',
)

MIDDLEWARE_CLASSES = (
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

ROOT_URLCONF = 'loki.urls'

WSGI_APPLICATION = 'loki.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'bg'

USE_I18N = True

USE_L10N = True

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (('bg', 'Bulgarian'),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, '../static')

AUTH_USER_MODEL = 'base_app.BaseUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'UPLOADED_FILES_USE_URL': False,
}

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# TODO: Just for the begining
CORS_ORIGIN_ALLOW_ALL = True

try:
    if 'TRAVIS' in os.environ:
        from .travis_settings import *
    else:
        from .local_settings import *
except ImportError:
    exit("{}_settings.py not found!".format("travis" if 'TRAVIS' in os.environ else "local"))


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}

EMAIL_BACKEND = 'post_office.EmailBackend'


TEMPLATE_CONTEXT_PROCESSORS = TCP + [
    'django.core.context_processors.request']


GRADER_GRADE_PATH = "/grade"
GRADER_CHECK_PATH = "/check_result/{buildID}/"
GRADER_GET_NONCE_PATH = "/nonce"
POLLING_SLEEP_TIME = 1  # seconds

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS
