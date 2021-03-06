# Django settings for schoolnetwork project.
import os
import sys
import djcelery

djcelery.setup_loader()
BROKER_URL = 'redis://localhost:6379/0'

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DIRNAME = os.path.abspath(os.path.dirname(__file__))
LIBPATH = os.path.join(DIRNAME, '..', 'lib')
sys.path.append(LIBPATH)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(DIRNAME, 'dev.db'),                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(DIRNAME, '..', 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(DIRNAME, '..', 'static')
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%_f%)x%nu)=(@zz)1-*t&amp;wa(71sy@39)8ic^&amp;0^oc%m0ap52&amp;2'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'schoolnetwork.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'schoolnetwork.wsgi.application'

TEMPLATE_DIRS = (
    (os.path.join(DIRNAME, '..', 'templates')),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount"
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.comments',
    'south',
    'avatar',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'imagekit',
    'postman',
    'pagination',
    'friendship',
    'django_wysiwyg',
    'djcelery',
    'jqchat',
    'app.timelines',
    'app.events',
    'app.userprofile',
    'app.academy',
    'app.connections',
    'app.groups',
    #'threadedcomments',
    #'django.contrib.comments',
)

#COMMENTS_APP = 'threadedcomments'

SOCIALACCOUNT_AVATAR_SUPPORT = 'avatar'

POSTMAN_DISALLOW_ANONYMOUS = True  # default is False
#POSTMAN_DISALLOW_MULTIRECIPIENTS = True # default is False
#POSTMAN_DISALLOW_COPIES_ON_REPLY = True # default is False
#POSTMAN_DISABLE_USER_EMAILING = True # default is False
POSTMAN_AUTO_MODERATE_AS = True  # default is None
POSTMAN_NOTIFIER_APP = 'notification'  # default is 'notification'
POSTMAN_MAILER_APP = 'mailer'  # default is 'mailer'
POSTMAN_AUTOCOMPLETER_APP = {
     'name': '',  # default is 'ajax_select'
    # 'field': '', # default is 'AutoCompleteField'
    # 'arg_name': '', # default is 'channel'
    # 'arg_default': 'postman_friends', # no default, mandatory to enable the feature
 }  # default is {}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_PROFILE_MODULE = 'accounts.Profile'

ACCOUNT_REQUIRED_EMAIL_DOMAIN = '.edu'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
        {
            'SCOPE': ['email', 'publish_stream', 'read_stream'],
            'METHOD': 'oauth2',
        }
    }

LOGIN_REDIRECT_URL = '/'
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: "/%s/" % u.username,
}
ACCOUNT_ACTIVATION_DAYS = 7
DEFAULT_FROM_EMAIL = 'SCHOOL NETWORK <schoolnetwork@sixceed.com>'
DEFAULT_CONTENT_EMAIL = "Thank you for your submitted questions. Our staff has received your questions and will be replied shortly"
DEFAULT_CONTENT_EMAIL_COURSE = "You have been invited to a new Course"
DEFAULT_CONTENT_EMAIL_GROUP = "You have been invited to a new Group"
DEFAULT_CONTENT_EMAIL_ASSIGNMENT = "Attention to all Students : the Professor has made a new Assignment"
DEFAULT_CONTENT_EMAIL_GRADE = "The Professor has gave grade"
DEFAULT_CONTENT_EMAIL_COMMENT = "You have a new comment on you post"

FACEBOOK_APPS_ID = '500336159997765'

CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0
CELERY_IMPORTS = ("app.events.notification", )
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERYD_LOG_FILE = '/tmp/celery.log'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_PASSWORD = 'testtest'
SERVER_EMAIL = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER = 'test@looksmi.com.ua'
EMAIL_PORT = 25


try:
    from local_settings import *
except ImportError:
    pass

