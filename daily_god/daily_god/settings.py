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
from django.utils.log import DEFAULT_LOGGING

import sys
import os
import logging

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_DIR = Path(PROJECT_ROOT, 'apps')

SITE_ID = 1



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv("DEBUG") == "on" else False

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS","127.0.0.1").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS","https://127.0.0.1").split(",")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Application definition

INSTALLED_APPS = [
    'frontend',
    'posts',
    'quotes',
    'api',
    'prayers',
    'comments',
    'profiles',
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
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "allauth_ui",
    'allauth',
    'allauth.account',
    'allauth.socialaccount.providers.google',
    'django_comments',
    'embed_video',
    "widget_tweaks",
    "slippers",
    "compressor",
]

# Django comments Settings
COMMENTS_APP='comments'


MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_browser_reload.middleware.BrowserReloadMiddleware",

    # CACHING
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",


    # HTMX
    'django_htmx.middleware.HtmxMiddleware',


    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

SITE_ID = 1
LOGIN_REDIRECT_URL = "/"  # new

ROOT_URLCONF = 'daily_god.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            Path(APP_DIR, 'frontend', 'templates'),
            Path(APP_DIR, 'frontend', 'templates', 'components'),
            Path(APP_DIR, 'templates'),
            Path(APP_DIR, 'templates', 'posts'),
            Path(APP_DIR, 'templates', 'quotes'),
            Path(APP_DIR, 'templates', 'prayers'),
            Path(APP_DIR, 'templates', 'profiles'),
            Path(APP_DIR, 'templates', 'comments'),
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
        "OPTIONS": {
            "pool": True,
        },
    }
}


cache_port = os.getenv("CACHE_PORT", default=11211)
cache_host = os.getenv("CACHE_HOST", default='127.0.0.1')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': f'{cache_host}:{cache_port}',
        'TIMEOUT': 60*60*3,
        "OPTIONS": {"MAX_ENTRIES": 1000},
    }
}

# cache settings
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 6000
CACHE_MIDDLEWARE_KEY_PREFIX = ''

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

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'compressor.finders.CompressorFinder',
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TAILWIND_APP_NAME = 'theme'

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

INTERNAL_IPS = [
    "127.0.0.1",
]


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Logging Settings

LOG_LEVEL = os.environ.get("LOG_LEVEL", logging.DEBUG if DEBUG else logging.WARNING)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'default': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-2s %(levelname)-2s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler" , "formatter": "default"},
        # A null handler ignores the message
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": 'WARNING',
        },
        # Our application code
        'app': {
            'level': LOG_LEVEL,
            'handlers': ['console'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        "django.security.DisallowedHost": {
            # Redirect these messages to null handler
            "handlers": ["null"],
            # Don't let them reach the root-level handler
            "propagate": False,
        },
    },
}

# All Auth Settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_SIGNUP_FORM_HONEYPOT_FIELD = "phone_number"
ACCOUNT_USERNAME_MIN_LENGTH = 3

# ALLAUTH UI Settings
ALLAUTH_UI_THEME = "dark"

# Django EMBED Video Settubgs
EMBED_VIDEO_BACKENDS = (
    'embed_video.backends.YoutubeBackend',
    'embed_video.backends.VimeoBackend',
)


# Seedling App Settings
TRUST_LEVEL_THRESHOLD = int(os.getenv("TRUST_LEVEL_THRESHOLD", 10))

#NPM_BIN_PATH = "/usr/local/bin/npm"

# TODO: Add Following Packages for Prod:
# django-comments-xtd
# django-defender
# django-filter
# django-ninja
# django-otp
# django-two-factor-auth
