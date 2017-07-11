import os.path
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

try:
    from settings_local import *
except ImportError:
    from settings_local_example import *

TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = ['texting.flatmaterooms.co.uk', 'localhost']
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX  = 'Texting centre: '
SERVER_EMAIL = DEFAULT_FROM_EMAIL

USE_I18N = USE_L10N = False
TIME_ZONE = 'Europe/London'
INTERNAL_IPS = ('127.0.0.1',)
SECRET_KEY = PROJECT_ROOT
ADMINS = MANAGERS = (('Admin', DEFAULT_FROM_EMAIL),)
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [PROJECT_ROOT + '/templates/',],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
        ]
    }
}]
MIDDLEWARE_CLASSES = ('paging.PagingMiddleware',)
ROOT_URLCONF = 'urls'
INSTALLED_APPS = ('sms',)
