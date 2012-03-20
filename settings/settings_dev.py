from default import *

LOGIN_URL = '/auth/login/'
LOGOUT_URL = '/auth/logout/'
LOGIN_REDIRECT_URL = '/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

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
    'int.debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',   
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# debug toolbar
INTERNAL_IPS = ('127.0.0.1',)
DEBUG_TOOLBAR_CONFIG = {
                        'INTERCEPT_REDIRECTS': False, 
                        }


DEBUG = True
TEMPLATE_DEBUG = DEBUG
