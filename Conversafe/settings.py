"""
Django settings for Conversafe project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#8!21y7^3x19hjn%me5@tiuvh=v!f1=0m_^q!4px(z1)4h#x48'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ["192.168.29.17"]

# Session details
INTERNAL_IPS = [
    "127.0.0.1",
]

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1440*60*15
PASSWORD_RESET_TIMEOUT_DAYS=1

#Email verification

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'emails.conversafe@gmail.com'
EMAIL_HOST_PASSWORD = 'zmhx zueq cjfz gguq'


EXPIRE_AFTER = "1d"

MAX_RETRIES = 4
DEFAULT_FROM_EMAIL = 'noreply<no_reply@conversafe.com>'


# Custom Email UI
LOGIN_URL = "login"

HTML_MESSAGE_TEMPLATE = "auth/email/emailTemplates/emailTemplate.html"

VERIFICATION_SUCCESS_TEMPLATE = "auth/email/showInfo/verificationSuccessful.html"

VERIFICATION_FAILED_TEMPLATE = "auth/email/showInfo/verificationFailed.html"

REQUEST_NEW_EMAIL_TEMPLATE = "auth/email/resendEmail.html"

LINK_EXPIRED_TEMPLATE = 'auth/email/showInfo/expired.html'

NEW_EMAIL_SENT_TEMPLATE  = 'auth/email/showInfo/checkEmail.html'



# Application definition

INSTALLED_APPS = [
    'daphne',
# Email Verification
    'verify_email.apps.VerifyEmailConfig',
# Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
# Other Django apps
    'landing',
    'core',
    'chat',
    # 'notification',

# Browser auto reload App
    # 'django_browser_reload'

    # Django notifications
    'notifications',
    'django_celery_beat'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Browser reload middleware
    # "django_browser_reload.middleware.BrowserReloadMiddleware"
]

ROOT_URLCONF = 'Conversafe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,"templates"],
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

WSGI_APPLICATION = 'Conversafe.wsgi.application'
ASGI_APPLICATION='Conversafe.asgi.application'


# Celery


CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# "BACKEND": "channels.layers.InMemoryChannelLayer"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
STATICFILES_DIRS = [BASE_DIR / "static/"]
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# User Auth model

AUTH_USER_MODEL = 'landing.AUser'

# default_app_config = 'full.python.path.to.your.app.foo.apps.FooConfig'