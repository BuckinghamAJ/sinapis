"""
Django settings for daily_god project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from django.db.utils import OperationalError
from django.db import connections
import environ
import sys
import os 
PROJECT_ROOT = Path(__file__).resolve().parent
APP_DIR = Path(PROJECT_ROOT, 'apps')

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Take environment variables from .env file
environ.Env.read_env(Path(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'frontend',
    'posts',
    'quotes',
    'api',
    'prayers',
    'comments',
    'template_partials',
    'taggit',
    'tailwind',
    'theme',
    "crispy_forms",
    "crispy_tailwind",
    'django_htmx',
    'django_browser_reload',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",

    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'daily_god.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            Path(APP_DIR, 'frontend', 'templates'),
            Path(APP_DIR, 'frontend', 'templates', 'components'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            "builtins": ["template_partials.templatetags.partials"],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'daily_god.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

def check_local_db():
    """Check if the local database is accessible."""
    try:
        db_connection = connections['default']
        db_connection.cursor()
        return True
    except OperationalError:
        return False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('LOCAL_DB_NAME'),
        'USER': env('LOCAL_DB_USER'),
        'PASSWORD': env('LOCAL_DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
        "OPTIONS": {
            "pool": True,
        },
    },
    'production': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('PRODUCTION_DB_NAME'),
        'USER': env('PRODUCTION_DB_USER'),
        'PASSWORD': env('PRODUCTION_DB_PASSWORD'),
        'HOST': env('PRODUCTION_DB_HOST'),
        'PORT': env('PRODUCTION_DB_PORT'),
        "OPTIONS": {
            "pool": True,
        },
    }
}

if not check_local_db():    
    # If the local database is not accessible, use the production database
    DATABASES['default'] = DATABASES['production']


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TAILWIND_APP_NAME = 'theme'

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

INTERNAL_IPS = [
    "127.0.0.1",
]



# TODO: Add Following Packages for Prod:
# django-defender
# django-filter
# django-ninja
# django-otp
# django-two-factor-auth
