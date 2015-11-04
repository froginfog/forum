# -*- coding:utf-8 -*-
"""
Django settings for second project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-)u&csuu(70juzb$7h2iji$ts6=5m=-@z=5*kj%2#&kul=!1im'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bbs',
    'django_summernote',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'second.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bbs.globe_context.allforms',
                'bbs.globe_context.islogin',
            ],
        },
    },
]

WSGI_APPLICATION = 'second.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bbs-db',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': '',
        'PORT': '3306'
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'Zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (

       # Put strings here, like "/home/html/static" or "C:/www/django/static".

       # Always use forward slashes, even on Windows.

       # Don't forget to use absolute paths, not relative paths.

       #os.path.join(BASE_DIR,  'static'),

   )
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DOMAIN = 'wrx1984.oicp.net'

EMAIL_HOST_USER = 'blizzarding@126.com'
EMAIL_HOST_PASSWORD = '+wrx44139487*'
EMAIL_HOST = 'smtp.126.com'
EMAIL_PORT = '25'
DEFAULT_CHARSET = 'utf-8'

POST_PER_PAGE = 15
REPLY_PER_PAGE = 15



SUMMERNOTE_CONFIG = {

    'iframe': False,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Change editor size
    'width': '90%',
    'height': '300',

    'prettifyHtml': True,

    # Need authentication while uploading attachments.
    'attachment_require_authentication': True,

    'lang': 'zh-CN',

    # Set external media files for SummernoteInplaceWidget.
    # !!! Be sure to put {{ form.media }} in template before initiate summernote.
    'inplacewidget_external_css': (
        '//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css',
        '//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css',
    ),
    'inplacewidget_external_js': (
        '//code.jquery.com/jquery-1.9.1.min.js',
        '//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js',
    ),
}