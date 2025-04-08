"""
Django settings for config project.

Generated by 'backend-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

import dj_database_url
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "b9mbf+mnjd$bzpsp6250ya@w!!7k^l-w^608!h%fnyv#0l(y*x")

DEBUG = bool(os.environ.get("DEBUG", True))

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.main",
    "django_ckeditor_5",
    'django_celery_beat',
    "django_celery_results",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
database_url = os.environ.get("DATABASE_URL", None)
# database_url = "postgresql://telegram_user:oZyVGt82Z3yl@localhost:5432/telegram_bot"
if database_url:
    db_from_env = dj_database_url.config(default=database_url, conn_max_age=600)
    DATABASES = {"default": db_from_env}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_PATH = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "6937963289:AAGnc7rpYw0ljMPnv73YKbjG_1-3wsoNT30")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "6573821562:AAGHIWKfmzl33ErebRgm_quHfgN8ZbW4U0I")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_LOCATION = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
EXTRA_SETTINGS_ADMIN_APP = "extra_settings"
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        'TIMEOUT': 4233600  # Set the default timeout to 604800 seconds (14 day)
    }
}

CSRF_TRUSTED_ORIGINS = ["http://*.zukhriddin.uz", "https://*.zukhriddin.uz", "https://zukhriddin.uz",
                        "http://188.120.254.216", "http://188.120.254.216:85",
                        "188.120.254.216",
                        "http://zukhriddin.uz", "https://4cfc-84-54-70-172.ngrok-free.app", "http://zukhriddin.uz:8003"]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['|', 'bold', '|', 'italic', '|', 'link', '|', 'underline', '|', ],
        'language': 'ru',
    },
}

# CELERY SETTINGS

CELERY_broker_url = REDIS_LOCATION
accept_content = ['application/json']
result_serializer = 'json'
task_serializer = 'json'
result_backend = 'django-db'
timezone = TIME_ZONE
result_extended = True

CELERY_BROKER_URL = REDIS_LOCATION
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_EXTENDED = True

# CELERY BEAT SCHEDULER

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "6573821562:AAGHIWKfmzl33ErebRgm_quHfgN8ZbW4U0I")
BOT_ID = 7098180147

MAX_UPLOAD_SIZE = 52428800
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800
import sentry_sdk

sentry_sdk.init(
    dsn="https://268e3d46702dcd5092d8d7172beaaae7@o4503918987837440.ingest.us.sentry.io/4507324413575168",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
