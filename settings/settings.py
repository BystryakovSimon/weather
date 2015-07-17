# -*- coding: utf-8 -*-
import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

os.environ["CELERY_LOADER"] = "django"

gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath('%s/../' % os.path.dirname(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, 'apps'))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'localdb.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
#USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
#USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
#USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(PROJECT_ROOT, "/static")
STATIC_URL = "/static/"

ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

ADMIN_TOOLS_INDEX_DASHBOARD = 'settings.dashboard.CustomIndexDashboard'

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '&alocx+iw^&yn$mlurvx&3cgoafe9^m8%fy18+_nl6)ce6e0&v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

ROOT_URLCONF = 'settings.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'settings.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

CMS_TEMPLATES = (
    ('main.html', u'Главная'),
)

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.admin',
    'djcelery',
    'djkombu',
    'django_extensions',

    'cms',
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.file',
    'cms.plugins.flash',
    'cms.plugins.link',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'cms.plugins.teaser',
    'cms.plugins.video',
    'cms.plugins.twitter',
    'cms.plugins.inherit',
    'mptt',
#    'publisher',
    'menus',

    'classytags',
    'html5lib',
    'sekizai',

    'lib',
#    'south',
    'weather',
#    'wparser',
)

import djcelery
djcelery.setup_loader()

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'bistrikovsemen@gmail.com'
EMAIL_HOST_PASSWORD = 'pw'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'myproject.custom': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        }
    }
}

LANGUAGES = (
    ('ru', gettext('Russia')),
)

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

BROKER_BACKEND = "djkombu.transport.DatabaseTransport"

TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'




#from celery import Celery
#from django.conf import settings
#wparser = Celery('settings')
##app.config_from_object('django.conf:settings')
##app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    'start-every-60-minutes': {
        'task': 'weather.tasks.WParser',
#        'schedule': timedelta(seconds=10),
#        'schedule': timedelta(hours=1),
        'schedule': timedelta(minutes=60),
#        'args': (16, 16)
    },
}

# Name of nodes to start
# here we have a single node
CELERYD_NODES="weather_node"
# or we could have three nodes:
#CELERYD_NODES="w1 w2 w3"

# Absolute path to "manage.py"
CELERY_BIN=PROJECT_ROOT+"/manage.py"

# How to call manage.py
#CELERYD_MULTI="celery multi"

# Extra command-line arguments to the worker
##CELERYD_OPTS="--time-limit=300 --concurrency=8"

# %N will be replaced with the first part of the nodename.
#CELERYD_LOG_FILE=PROJECT_ROOT+"/celery/weather_log.log"
#CELERYD_PID_FILE=PROJECT_ROOT+"/celery/weather.pid"
#
## CELERY SETTINGS
#BROKER_URL = 'redis://localhost:6379/0'
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = 'Europe/Moscow'

#Reserve one task at a time
#CELERY_ACKS_LATE = True
#CELERYD_PREFETCH_MULTIPLIER = 1

# Extra arguments to celeryd
#CELERYD_OPTS="--concurrency=1"