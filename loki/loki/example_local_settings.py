# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=jpbhxfh_$%xh-%q2*@$#g)1%tvvgu3v_z6@qmf#+r+y=1gy9y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = ''
EMAIL_PORT = 123
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

DJOSER = {
    'DOMAIN': 'frontend.com',
    'SITE_NAME': 'Frontend',
    'PASSWORD_RESET_CONFIRM_URL': '#/password_reset/{uid}/{token}',
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'LOGIN_AFTER_ACTIVATION': True,
    'SEND_ACTIVATION_EMAIL': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

MEDIA_URL = '/media/'

CKEDITOR_UPLOAD_PATH = "uploads/"

CHECKIN_TOKEN = 'TOKEN FROM CHECKIN SYSTEM HERE'

GITHUB_OATH_TOKEN = 'TOEK FROM GITHUB HERE'

GRADER_ADDRESS = "http://IP_HERE"

GRADER_API_KEY = ""

GRADER_API_SECRET = ""

# Celery settings

BROKER_URL = 'amqp://guest:guest@localhost//'

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'retest-solutions-on-test-change': {
        'task': 'education.tasks.check_for_retests',
        'schedule': timedelta(minutes=1),
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'loki_cache',
        'TIMEOUT': 60 * 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}
