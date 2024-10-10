"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.9.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#b%*nd5n$xqxe-&5=&22*bo)g^o!0c6!z+c(i)r!y86@%b3i*0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # базовый функционал
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # добаленные приложения
    'users',
    'dogs',

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

WSGI_APPLICATION = 'config.wsgi.application'


load_dotenv()
USER = os.getenv('MS_SQL_USER')
PASSWORD = os.getenv('MS_SQL_KEY')
HOST = os.getenv('MS_SQL_SERVER')
DATABASE = os.getenv('MS_SQL_DATABASE')

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': DATABASE,
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': HOST,
        'PORT': '',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server'
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    BASE_DIR / 'static',
)
"""django.views.static.serve()
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
прописывается config.urls.py"""

MEDIA_URL = '/media/'
MEDIA_ROOT = (
    BASE_DIR / 'media',
)

"""Во время разработки вы можете обслуживать загруженные пользователем медиафайлы из MEDIA_ROOT,
используя предоставленные django.views.static.serve().
Например, если ваш MEDIA_URLопределен как /media/, вы можете сделать это,
добавив следующий фрагмент к вашему ROOT_URLCONF: 
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)"""
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'
