﻿"""
Django settings for agency project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
db_from_env = dj_database_url.config()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wz-vrmuk9a&8vs+)r5n*j7*oce$*z&rl77os=#8%#tp)&xs%m3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'concert-agency.onrender.com',]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'concert',
    'django_cleanup',
    'widget_tweaks',
    'crispy_forms',
    'crispy_bootstrap4',
    'rest_framework',
    #'cloudinary_storage',
    #'cloudinary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',    
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ROOT_URLCONF = 'agency.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'agency.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': BASE_DIR / 'db.sqlite3',
    #}

    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #    'NAME': 'agency',
    #    'USER' : 'customer',
    #    'PASSWORD' : 'customer',
    #    'HOST' : '127.0.0.1',
    #    'PORT' : '5432',
    #}
    
    'default': {
	    'ENGINE': 'django.db.backends.postgresql_psycopg2',
	    'NAME': 'agency_tqxh',
	    'USER' : 'agency_admin',
	    'PASSWORD' : 'EYJxyrJ9Un7Fry2itDPVstTsEMutc6OW',
	    'HOST' : 'dpg-cmfa4racn0vc73c194qg-a.frankfurt-postgres.render.com',
	    'PORT' : '5432',
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

LANGUAGE_CODE = 'ru-Ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True 

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

LANGUAGES = (
    ('kk', 'Kazakh'),
    ('ru', 'Russian'),    
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, "static"),
#]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MEDIA_ROOT - это абсолютный путь файловой системы к каталогу для загруженных пользователем файлов.
# MEDIA_URL - это URL-адрес, который можно использовать в наших шаблонах для файлов.
# Папку media необходимо создать в корневой папке проекта
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
MEDIA_URL = '/media/'

# Redirect to home URL after login (Default redirects to /accounts/profile/)
# Теперь, при входе в систему, вы по умолчанию должны перенаправляться на домашнюю страницу сайта а не на /accounts/profile/
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_REDIRECT_URL = '/'
LOGOUT_URL = '/logout/'

# Сохранения изображения
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dw2ghvqzm',
    'API_KEY': '556392947926318',
    'API_SECRET': '4aNS89EKX40AQulEd8A8_D0bK-k',
}
#DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Сброс пароля по E-Mail
EMAIL_TIMEOUT = 300

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = 'shop260222@mail.ru' 
EMAIL_HOST_PASSWORD = 'Nn27t2PMDiJ7rSqWeFuw'
DEFAULT_FROM_EMAIL  = 'shop260222@mail.ru'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER