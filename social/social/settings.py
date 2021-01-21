"""
Django settings for social project.

Generated by 'django-admin startproject' using Django 3.0.11.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from django.urls import reverse_lazy

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUTHENTICATION_BACKENDS = [
'django.contrib.auth.backends.ModelBackend',

'social_core.backends.google.GoogleOAuth2',
'account.authentication.EmailAuthBackend',
'social_core.backends.facebook.FacebookOAuth2',
]
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

SECRET_KEY = '&(@_+3wr=ak*227&cypmuox5ls@p7(coy-+=#i(kq9^ub0kfdz'
#google auth 
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1020048329204-cpo6l1cnu1rq8fdo134mo4c2pcmhtdeu.apps.googleusercontent.com' # Google Consumer Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'kVcAnJ96BwtY0d92lbh0EbKW' # Google Consumer Secret
#facebook social authentication
SOCIAL_AUTH_FACEBOOK_KEY = '183911986707376' # Facebook App ID
SOCIAL_AUTH_FACEBOOK_SECRET = 'f8f00b9a341f3b63f7a352f41ed6e350' # Facebook App Secret
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ABSOLUTE_URL_OVERRIDES = {
'auth.user': lambda u: reverse_lazy('user_detail',
args=[u.username])
}

ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Application definition

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'agrictime@gmail.com'
EMAIL_HOST_PASSWORD = 'S45607899j'
EMAIL_PORT = 587

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'blog.apps.BlogConfig',
    'taggit',
    'social_django',
    'django_extensions',
    'images.apps.ImagesConfig',
    'easy_thumbnails',
    'actions.apps.ActionsConfig',
    'mptt',
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

ROOT_URLCONF = 'social.urls'

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

WSGI_APPLICATION = 'social.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
PASSWORD_RESET = 'password_reset_form'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

FROM_EMAIL = 'okonkwostanley67@yahoo.com'
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')