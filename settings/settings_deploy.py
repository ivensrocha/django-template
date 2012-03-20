from default import *

DEPLOY_PREFIX = '/novo'

LOGIN_URL = DEPLOY_PREFIX + '/auth/login/'
LOGOUT_URL = DEPLOY_PREFIX + '/auth/logout/'
LOGIN_REDIRECT_URL = DEPLOY_PREFIX + '/'

ADMIN_MEDIA_PREFIX = DEPLOY_PREFIX + STATIC_URL + '/admin/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'int.core',
    'int.myAuth',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',   
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

DEBUG = False
TEMPLATE_DEBUG = DEBUG
