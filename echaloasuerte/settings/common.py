"""Common settings and globals."""

import sys
from os.path import abspath, basename, dirname, join, normpath
from django.utils.translation import ugettext_lazy as _

########## PATH CONFIGURATION
# Absolute filesystem path to this Django project directory.
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Site name.
SITE_NAME = basename(DJANGO_ROOT)

# Absolute filesystem path to the top-level project folder.
SITE_ROOT = dirname(DJANGO_ROOT)

# Absolute filesystem path to the secret file which holds this project's
# SECRET_KEY. Will be auto-generated the first time this file is interpreted.
SECRET_FILE = normpath(join(SITE_ROOT, 'deploy', 'SECRET'))

# Add all necessary filesystem paths to our system path so that we can use
# python import statements.
sys.path.append(SITE_ROOT)
sys.path.append(normpath(join(DJANGO_ROOT, 'apps')))
sys.path.append(normpath(join(DJANGO_ROOT, 'libs')))
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# Disable debugging by default.
DEBUG = False
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# Admin and managers for this project. These people receive private site
# alerts.
ADMINS = (
    ('David Naranjo', 'dnaranjo89@gmail.com'),
    ('Mario Corchero', 'mariocj89@gmail.com'),
    ('Facebook', 'echaloasuerte.admins@groups.facebook.com'),
)

MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## GENERAL CONFIGURATION
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name although not all
# choices may be available on all operating systems. On Unix systems, a value
# of None will cause Django to use the same timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html.
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('es', _('Spanish')),
    ('en', _('English')),
)

# The ID, as an integer, of the current site in the django_site database table.
# This is used so that application data can hook into specific site(s) and a
# single database can manage content for multiple sites.
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

USE_TZ = True
########## END GENERAL CONFIGURATION

LOCALE_PATHS = (
    normpath(join(SITE_ROOT, 'locale')),
)


########## MEDIA CONFIGURATION
# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# URL that handles the media served from MEDIA_ROOT.
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# Absolute path to the directory static files should be collected to. Don't put
# anything in this directory yourself; store your static files in apps' static/
# subdirectories and in STATICFILES_DIRS.
STATIC_ROOT = '/data/apache/serve/echaloasuerte/static'

# URL prefix for static files.
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files.
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# List of finder classes that know how to find static files in various
# locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'
########## END STATIC FILE CONFIGURATION


########## TEMPLATE CONFIGURATION
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

# Directories to search when loading templates.
TEMPLATE_DIRS = (
    normpath(join(DJANGO_ROOT, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
MIDDLEWARE_CLASSES = (
    'server.middleware.exception_mdw.ExceptionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'echaloasuerte.logging_mw.RequestLoggerMiddleware',
)
########## END MIDDLEWARE CONFIGURATION

AUTHENTICATION_BACKENDS = ('server.backends.authentication.EchaloasuerteAuthBE',)

########## APP CONFIGURATION
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'tastypie',

    'server',
    'web',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.tz",
                               "django.contrib.messages.context_processors.messages",
                               "server.context_processors.google_analytics")

########## END APP CONFIGURATION

########## CRISPY FORMS
CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_FAIL_SILENTLY = not DEBUG
########## END CRISPY FORMS

########## URL CONFIGURATION
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## KEY CONFIGURATION
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$a3e(-u8)4m4*(vfnfnfjba@bd13-2u#=(i$*7(p!(6ck0ugd='
########## END KEY CONFIGURATION

# Fixing 1_6.W001
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Allowed host to be used
ALLOWED_HOSTS = [
    '.etcaterva.com',
    '.etcaterva.com.',
    '.pickforme.net',
    '.pickforme.net.',
    '.onlinewbs.com',
    '.onlinewbs.com.',  # Also allow FQDN and subdomains
    '.echaloasuerte.com',
    '.echaloasuerte.com.',
    '92.222.219.42',
    'vps71464.ovh.net',
    'vps162180.ovh.net',
    '92.222.28.167',
]

LOGIN_URL = "/accounts/sigin/"

#EMAIL settings
DEFAULT_FROM_EMAIL = "echaloasuerte@gmail.com"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = "echaloasuerte@gmail.com"
EMAIL_HOST_PASSWORD = 'GMAIL_PASSWORD_PLACEHOLDER'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = "[django][echaloasuerte] "  #for admin mails
SERVER_EMAIL = "echaloasuerte@gmail.com"
