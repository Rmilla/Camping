"""
Django settings for WebCamping project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

 
from pathlib import Path
import os
import environ
from django.contrib.auth import get_user_model
from django.conf import settings
from corsheaders.middleware import CorsMiddleware
from django.contrib.staticfiles import handlers

# extend StaticFilesHandler to add "Access-Control-Allow-Origin" to every response
class CORSStaticFilesHandler(handlers.StaticFilesHandler):
    def serve(self, request):
        response = super().serve(request)
        response['Access-Control-Allow-Origin'] = '*'
        return response

# monkeypatch handlers to use our class instead of the original StaticFilesHandler
handlers.StaticFilesHandler = CORSStaticFilesHandler


# class CorsMiddleware(CorsMiddleware):
#     def process_request(self, request):
#         response = super().process_request(request)
#         response['Access-Control-Allow-Origin'] = '*'
#         return response

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
 
# CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
]
CORS_ALLOW_HEADERS = [
    'Authorization',  # Autorise l'en-tête Authorization
    'Content-Type',  # Autorise l'en-tête Content-Type
    'Accept',  # Autorise l'en-tête Accept
]
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
]
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
 
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
 
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
 
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
 
ALLOWED_HOSTS = ["127.0.0.1", ""]

STATIC_URL = '/static/'
STATICFILES_DIRS = [
         "C:/Projets/Stage/Camping/WebCamping/camping/static",
         ]
""""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'camping',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""


# Application definition
DATABASES ={'default':
{
'ENGINE': env.str('DB_ENGINE'),
'NAME':env.str('DB_NAME'),
'USER':env.str('DB_USER'),
'PASSWORD':env.str('DB_PASSWORD'),
'HOST':env.str('DB_HOST'),
'PORT':env.int('DB_PORT')
}
}


 
INSTALLED_APPS = [
    "corsheaders",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    #"rest_framework.authtoken",
    'rest_framework_simplejwt',
    "django_filters",
    "camping",
    "admin_honeypot",
    "axes",   
    
]

 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # Default Django authentication backend
    'rest_framework.authentication.TokenAuthentication', # Token-based authentication for API
    "axes.backends.AxesStandaloneBackend",
]
 
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "axes.middleware.AxesMiddleware",
    
]



ROOT_URLCONF = 'WebCamping.urls'
 
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
 
WSGI_APPLICATION = 'WebCamping.wsgi.application'
 
 
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'camping.Login'

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
 
LANGUAGE_CODE = 'en-us'
 
TIME_ZONE = 'UTC'
 
USE_I18N = True
 
USE_TZ = True
 
 
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
 
STATIC_URL = 'static/'
 
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
 
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AXES_COOLOE_NAME = '.axes/cache'
AXES_FAILURE_LIMIT = 5  # Number of failed attempts before a user is locked out
AXES_COOLOE_AGE = 86400  # 1 day
AXES_LOCK_OUT_BY_COMBINATION = True