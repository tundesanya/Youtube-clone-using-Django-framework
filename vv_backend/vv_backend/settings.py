"""
Django settings for vv_backend project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from configparser import ConfigParser

config = ConfigParser()
config.read('../config/config.ini')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['Django']['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config['Django'].getboolean('DEBUG')

ALLOWED_HOSTS = config['Django']['ALLOWED_HOSTS'].split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Additional Apps:
    'django_extensions',
    'django_countries',
    'rest_framework',
    'knox',

    # Project Apps:
    'content',
    'user_interactions',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vv_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'vv_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config['PostgreSQL']['DBNAME'],
        'HOST': config['PostgreSQL']['HOST'],
        'PORT': config['PostgreSQL']['PORT'],
        'USER': config['PostgreSQL']['USER'],
        'PASSWORD': config['PostgreSQL']['PASSWORD']
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Ziming: since we override the default django user model, we need this to make sure our
# own model is used for authentication
AUTH_USER_MODEL = 'users.User'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# TODO: Nishil: Remove this once profile pictures are moved to S3
# To store profile pictures
MEDIA_ROOT = BASE_DIR / 'assets/profile_pictures'
MEDIA_URL = '/assets/profile_pictures/'


# Django REST Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
    ),

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 2,
    # NOTE: Nishil: Don't know how useful this is, but it's here if we need it.
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    # ),



    # NOTE: To disable the browsable API in production
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ) if not DEBUG else (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}


# Django Rest Knox
# https://jazzband.github.io/django-rest-knox/settings/

REST_KNOX = {
    'TOKEN_TTL': timedelta(hours=10),
    'AUTO_REFRESH': True,
    'MIN_REFRESH_INTERVAL': 60 * 60 * 5,    # 5 hours
    # 'USER_SERIALIZER': 'users.serializers.UserLoginSerializer', # Default is knox.serializers.UserSerializer which works fine and dynamically for our custom user model
    # 'AUTH_HEADER_PREFIX': 'Bearer',                             # Default is 'Token'

    # NOTE: Below settings should keep the user logged in permanently but don't know the implications of this.
    # 'TOKEN_TTL': None,
    # 'AUTO_REFRESH': True,
    # 'MIN_REFRESH_INTERVAL': 60 * 60 * 24 * 7, # 7 days
}

# Google OAuth2 credentials from Google Developer Console
GOOGLE_OAUTH = {
    'client_id': config['Google']['OAUTH2_CLIENT_ID'],
    'client_secret': config['Google']['OAUTH2_CLIENT_SECRET'],
    'redirect_uri': config['Google']['OAUTH2_REDIRECT_URI']
}


# NTFY Topic for verification email testing
DHOST_URL = config['Development']['DHOST_URL']
NTFY_TOPIC = config['Development']['NTFY_TOPIC']