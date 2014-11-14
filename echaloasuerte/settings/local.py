"""Local settings and globals."""
from echaloasuerte.settings.common import *


########## DEBUG CONFIGURATION
DEBUG = True
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION

########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': normpath(join(SITE_ROOT, 'default.db')),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION