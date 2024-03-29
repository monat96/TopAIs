"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import json
import os
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

secret_file = os.path.join(BASE_DIR, 'secrets.json')
db_file = os.path.join(BASE_DIR, 'databases.json')
email_file = os.path.join(BASE_DIR, 'email.json')
# secret_file = [BASE_DIR /'secrets.json']

with open(secret_file) as f:
    secret = json.loads(f.read())
with open(db_file) as f:
    db = json.loads(f.read())

with open(email_file) as f:
    email = json.loads(f.read())


def get_secret(setting, secrets=secret):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'app',
    'accounts',
    'board',
    'map',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# 외부 db
# DATABASES = {
#     'default': {
#         'ENGINE': db.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
#         'NAME': db.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
#         'USER': db.get('SQL_USER', 'user'),
#         'PASSWORD': db.get('SQL_PASSWORD', 'password'),
#         'HOST': db.get('SQL_HOST', 'localhost'),
#         'PORT': db.get('SQL_PORT', '5432'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'ENGINE': db.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        # 'NAME': db.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
        # 'USER': db.get('SQL_USER', 'user'),
        # 'PASSWORD': db.get('SQL_PASSWORD', 'password'),
        # 'HOST': db.get('SQL_HOST', 'localhost'),
        # 'PORT': db.get('SQL_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email 전송 설정
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'        # 개발용으로, 실제로 이메일을 보내지 않고 console에 출력되도록 함. (이메일이 잘 출력되는지 확인)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # 배포용으로, 실제로 이메일 전송됨.

EMAIL_HOST = 'smtp.gmail.com'  # 메일을 호스트하는 서버
EMAIL_PORT = '587'  # gmail과 통신하는 포트
EMAIL_USE_TLS = True  # TLS 보안 방법
EMAIL_HOST_USER = email["EMAIL_HOST_USER"]  # 발신할 이메일
EMAIL_HOST_PASSWORD = email["EMAIL_HOST_PASSWORD"]  # 발신할 메일의 비밀번호
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # 사이트와 관련한 자동 응답을 받을 이메일 주소

# user 관련 설정
AUTH_USER_MODEL = 'accounts.User'
LOGOUT_REDIRECT_URL = '/'

# media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# session 설정
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True
