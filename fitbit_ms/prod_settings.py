import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = 'main/static/'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split()

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

#hostname = os.environ['DBHOST']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': os.environ['DBHOST'],
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'],
        'OPTIONS': {'sslmode': 'require'},
    },
}


#logging, log both to console and to file log at the INFO level
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'info_format': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
            }
        },
    'handlers': {
        'console': {
            'level':'INFO',
            'class': 'logging.StreamHandler',
        },
       'logfile': {        
           'level':'INFO', 
           'class': 'logging.handlers.RotatingFileHandler',
           'filename': os.environ['LOG_LOCATION'],
           'maxBytes': 10485760,           #10 mb
           'backupCount' : 5,
           'formatter' : 'info_format',
           'delay': True,
       },
    },
    'loggers': {
        'django': {
            'handlers':['console','logfile'],
            'propagate': True,
            'level':'INFO',
        },
        'django.db.backends': {
            'handlers': ['console','logfile'],
            'level': 'INFO',
            'propagate': False,
        },
        'main': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',           
        },
        'django_cron': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',           
        },
    },
}

#simulate sending without sending live email
SIMULATE_SEND = False

#emails
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'   #log email to console
EMAIL_HOST = 'exchange.chapman.edu'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_USER_NAME = 'ESI Recruiter, Chapman University'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 600
DEFAULT_FROM_EMAIL = os.environ['EMAIL_HOST_USER']
EMAIL_TEST_ACCOUNT = os.environ['EMAIL_TEST_ACCOUNT']          #all outgoing email sent here when in debug mode
