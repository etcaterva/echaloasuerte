from echaloasuerte.settings.common import *

#WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME


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

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
##########
BASE_LOG_PATH = join(SITE_ROOT, 'logs/')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s %(name)s.%(module)s.%(funcName)s | %(message)s',
            'datefmt' : '%Y%m%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            },
    },
    'loggers': {
        'django.request': {
            'handlers': [],
            'level': 'DEBUG',
            'propagate': False,
        },
        'echaloasuerte': {
            'handlers': [],
            'level': 'DEBUG',
            'propagate': False,
            },
    }
}
########## END LOGGING CONFIGURATION

#Mongo db configuration list
MONGO_END_POINTS = [
        {'host':'localhost', 'port':27017, 'database':'testing'},
        ]
