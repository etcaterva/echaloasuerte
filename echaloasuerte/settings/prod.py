from echaloasuerte.settings.common import *
import os

# WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME


########## DEBUG CONFIGURATION
DEBUG = False
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
BASE_LOG_PATH = os.environ.get("ECHALOASUERTE_LOGS_PATH", "/var/log/echaloasuerte/")
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(filename)s %(lineno)s %(message)s',
        },
        'standard': {
            'format': '[%(asctime)s] %(levelname)s %(name)s.%(module)s.%(funcName)s | %(message)s',
            'datefmt': '%Y%m%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'log_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(BASE_LOG_PATH, 'echaloasuerte_log.txt'),
            'maxBytes': 1024 * 1024 * 30,  # 30 MB
            'backupCount': 5,
        },
        'error_log_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(BASE_LOG_PATH, 'echaloasuerte_err.txt'),
            'maxBytes': 1024 * 1024 * 30,  # 30 MB
            'backupCount': 5,
        },
        'debug_log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.join(BASE_LOG_PATH, 'echaloasuerte_debug.txt'),
            'maxBytes': 1024 * 1024 * 30,  # 30 MB
            'backupCount': 5,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['debug_log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'echaloasuerte': {
            'handlers': ['log_file', 'error_log_file', 'debug_log_file', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
########## END LOGGING CONFIGURATION

# Mongo db configuration list
MONGO_END_POINTS = [
    {'host': 'localhost', 'port': 27017, 'database': 'prod'},
]

# Template caching
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 60  # 1 MINUTE
    }
}

GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-62791775-2'
