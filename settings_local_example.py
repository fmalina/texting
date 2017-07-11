DEBUG = True

# Database credentials
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'texting.db',
    }
}

# Email alerts over Gmail
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

# Used to send daily reports
DEFAULT_FROM_EMAIL = ''
MANAGER_PHONE = '' # comma separate multiple numbers

# see settings.py for more options