from dobrodzieje.settings.base import *

# Override base.py settings here

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# export DJANGO_SETTINGS_MODULE=dobrodzieje.settings.dev

SECRET_KEY = 'django-insecure-^a!=*niyi*mcg#1j@az#k2txrv!@m_e+gho_&2tl0&=$zw3!k3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# INTERNAL_IPS = [
#     '127.0.0.1',
# ]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
     'default': {
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': 'dev', 
        'USER': 'dev',
        'PASSWORD': 'dev',
        'HOST':'localhost',
        'PORT': '5432',
    }
}

# Static files (CSS, JavaScript, Images)
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Media Files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Chat
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}
