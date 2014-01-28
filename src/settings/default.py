# -*- coding: utf-8 -*-

"""
    Default settings
    Author  :   Alvaro Lizama Molina <alvaro@knoudo.com>
"""

import os.path
import sys


##
## Paths
##
DIRNAME = os.path.dirname(os.path.dirname(__file__))


##
## I18N & L18N
##
TIME_ZONE = 'America/Mexico_City'
LANGUAGE_CODE = 'es-es'
USE_I18N = True
USE_L10N = True
USE_TZ = True


##
## Security
##
SECRET_KEY = 'hcyf!<secret key here>'


##
## URL's
##
ROOT_URLCONF = 'urls'


##
## Deploy
##
WSGI_APPLICATION = 'wsgi.application'


##
## Domains
##
SITE_ID = 1
ALLOWED_HOSTS = ["*"]


##
## Middlewares
##
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
)


##
## Media & Statics
##
MEDIA_ROOT = os.path.join(DIRNAME, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(DIRNAME, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(DIRNAME, 'assets'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'


##
## Templates
##
TEMPLATE_LOADERS = (
    'django.template.loaders.eggs.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.debug',
    'django.contrib.messages.context_processors.messages',
    "django.contrib.auth.context_processors.auth",
)


##
## Apps
##
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'debug_toolbar',
    'pipeline',
    'applications.front'
)


##
## Django Debug Tool Bar
##
INTERNAL_IPS = ('10.0.2.2',)


##
## Pipeline
##
PIPELINE_CSS = {
    'stylesheets': {
        'source_filenames': (
            'components/bootstrap/dist/css/bootstrap.min.css',
        ),
        'output_filename': 'stylesheets.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}
PIPELINE_JS = {
    'scripts': {
        'source_filenames': (
            'components/jquery/jquery.min.js',
            'components/bootstrap/dist/js/bootstrap.min.js',
        ),
        'output_filename': 'scripts.js',
    }
}


##
## Logs
##
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


##
## Settings
##
try:
    from enviroment import *
except:
    print "Copy enviroment.py.txt to enviroment.py"
    sys.exit(0)
