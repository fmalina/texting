DEBUG = True

# Database credentials
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'texting.db',
    }
}

# Campaign integration settings
TEXTING_RUN = 1  # Texts are not saved nor sent if RUN is 0
TEXTING_API_KEY = '********'
TEXTING_API_URL = 'https://example.com/api/my_categorised_numbers?key=' +\
                  TEXTING_API_KEY

# Email alerts over Gmail
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

# Used to send daily reports
DEFAULT_FROM_EMAIL = ''
MANAGER_PHONE = '' # comma separates multiple numbers
