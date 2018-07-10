'''
Django settings for sso-profile project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
'''

import os

import environ


env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

# As the app is running behind a host-based router supplied by Heroku or other
# PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']

APPEND_SLASH = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'raven.contrib.django.raven_compat',
    'django.contrib.sessions',
    'django.contrib.contenttypes',  # required by DRF, not using any DB
    'django.contrib.auth',
    'core',
    'directory_constants',
    'directory_components',
    'profile',
    'profile.api',
    'directory_healthcheck',
    'health_check',
    'export_elements',
]

MIDDLEWARE_CLASSES = [
    'directory_components.middleware.MaintenanceModeMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'sso.middleware.SSOUserMiddleware',
    'directory_components.middleware.NoCacheMiddlware',
    'directory_components.middleware.RobotsIndexControlHeaderMiddlware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'sso.context_processors.sso_processor',
                'directory_components.context_processors.urls_processor',
                ('directory_components.context_processors.'
                 'header_footer_processor'),
                'directory_components.context_processors.sso_processor',
                'directory_components.context_processors.analytics',
                'directory_components.context_processors.feature_flags',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# # Database
# hard to get rid of this
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Static files served with Whitenoise and AWS Cloudfront
# http://whitenoise.evans.io/en/stable/django.html#instructions-for-amazon-cloudfront
# http://whitenoise.evans.io/en/stable/django.html#restricting-cloudfront-to-static-files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_HOST = env.str('STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Logging for development
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }
else:
    # Sentry logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': (
                    'raven.contrib.django.raven_compat.handlers.SentryHandler'
                ),
                'tags': {'custom-tag': 'x'},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }


# directory-external-api
DIRECTORY_API_EXTERNAL_CLIENT_CLASSES = {
    'default': 'directory_api_external.client.DirectoryAPIExternalClient',
    'unit-test': (
        'directory_api_external.dummy_client.DummyDirectoryAPIExternalClient'
    ),
}
DIRECTORY_API_EXTERNAL_CLIENT_CLASS_NAME = env.str(
    'DIRECTORY_API_EXTERNAL_CLIENT_CLASS_NAME', 'default'
)
DIRECTORY_API_EXTERNAL_CLIENT_CLASS = DIRECTORY_API_EXTERNAL_CLIENT_CLASSES[
    DIRECTORY_API_EXTERNAL_CLIENT_CLASS_NAME
]
DIRECTORY_API_EXTERNAL_SIGNATURE_SECRET = env.str(
    'DIRECTORY_API_EXTERNAL_SIGNATURE_SECRET', ''
)
DIRECTORY_API_EXTERNAL_CLIENT_BASE_URL = env.str(
    'DIRECTORY_API_EXTERNAL_CLIENT_BASE_URL'
)

# directory-sso
SSO_PROXY_API_CLIENT_BASE_URL = env.str('SSO_PROXY_API_CLIENT_BASE_URL')
SSO_PROXY_SIGNATURE_SECRET = env.str('SSO_PROXY_SIGNATURE_SECRET')
SSO_PROXY_LOGIN_URL = env.str('SSO_PROXY_LOGIN_URL')
SSO_PROXY_LOGOUT_URL = env.str('SSO_PROXY_LOGOUT_URL')
SSO_PROXY_SIGNUP_URL = env.str('SSO_PROXY_SIGNUP_URL')
SSO_PROXY_PASSWORD_RESET_URL = env.str('SSO_PROXY_PASSWORD_RESET_URL')
SSO_PROXY_REDIRECT_FIELD_NAME = env.str('SSO_PROXY_REDIRECT_FIELD_NAME')
SSO_PROXY_SESSION_COOKIE = env.str('SSO_PROXY_SESSION_COOKIE')
SSO_PROFILE_URL = env.str('SSO_PROFILE_URL')
SSO_PROXY_API_OAUTH2_BASE_URL = env.str('SSO_PROXY_API_OAUTH2_BASE_URL')

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', True)
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', 16070400)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# HEADER AND FOOTER LINKS
HEADER_FOOTER_URLS_GREAT_HOME = env.str('HEADER_FOOTER_URLS_GREAT_HOME', '')
HEADER_FOOTER_URLS_FAB = env.str('HEADER_FOOTER_URLS_FAB', '')
HEADER_FOOTER_URLS_SOO = env.str('HEADER_FOOTER_URLS_SOO', '')
HEADER_FOOTER_URLS_EVENTS = env.str('HEADER_FOOTER_URLS_EVENTS', '')
HEADER_FOOTER_URLS_CONTACT_US = env.str('HEADER_FOOTER_URLS_CONTACT_US', '')
HEADER_FOOTER_URLS_DIT = env.str('HEADER_FOOTER_URLS_DIT', '')

# Sentry
RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_DSN', ''),
}

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', True)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

# Google tag manager
GOOGLE_TAG_MANAGER_ID = env.str('GOOGLE_TAG_MANAGER_ID')
GOOGLE_TAG_MANAGER_ENV = env.str('GOOGLE_TAG_MANAGER_ENV', '')
UTM_COOKIE_DOMAIN = env.str('UTM_COOKIE_DOMAIN')


EXPORTING_OPPORTUNITIES_API_BASIC_AUTH_USERNAME = env.str(
    'EXPORTING_OPPORTUNITIES_API_BASIC_AUTH_USERNAME', ''
)
EXPORTING_OPPORTUNITIES_API_BASIC_AUTH_PASSWORD = env.str(
    'EXPORTING_OPPORTUNITIES_API_BASIC_AUTH_PASSWORD', ''
)
EXPORTING_OPPORTUNITIES_API_BASE_URL = env.str(
    'EXPORTING_OPPORTUNITIES_API_BASE_URL'
)
EXPORTING_OPPORTUNITIES_API_SECRET = env.str(
    'EXPORTING_OPPORTUNITIES_API_SECRET'
)
EXPORTING_OPPORTUNITIES_SEARCH_URL = env.str(
    'EXPORTING_OPPORTUNITIES_SEARCH_URL'
)

# find a buyer
FAB_REGISTER_URL = env.str('FAB_REGISTER_URL')
FAB_EDIT_COMPANY_LOGO_URL = env.str('FAB_EDIT_COMPANY_LOGO_URL')
FAB_EDIT_PROFILE_URL = env.str('FAB_EDIT_PROFILE_URL')
FAB_ADD_CASE_STUDY_URL = env.str('FAB_ADD_CASE_STUDY_URL')
FAB_ADD_USER_URL = env.str('FAB_ADD_USER_URL')
FAB_REMOVE_USER_URL = env.str('FAB_REMOVE_USER_URL')
FAB_TRANSFER_ACCOUNT_URL = env.str('FAB_TRANSFER_ACCOUNT_URL')

HEADER_FOOTER_CONTACT_US_URL = env.str(
    'HEADER_FOOTER_CONTACT_US_URL',
    'https://contact-us.export.great.gov.uk/directory',
)

# feature flags
FEATURE_FLAGS = {
    # used by directory-components
    'MAINTENANCE_MODE_ON': env.bool('FEATURE_MAINTENANCE_MODE_ENABLED', False),
    # used by directory-components
    'SEARCH_ENGINE_INDEXING_OFF': env.bool(
        'FEATURE_SEARCH_ENGINE_INDEXING_DISABLED', False
    )
}

# healthcheck
HEALTH_CHECK_TOKEN = env.str('HEALTH_CHECK_TOKEN')
