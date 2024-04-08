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
from mongoengine import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
 
 
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
 
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
 
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
 
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
 
ALLOWED_HOSTS = ["127.0.0.1"]
 
# MongoDB settings

disconnect()
"""""
def test_connection():
    # Replace <your_connection_string> with your actual MongoDB Atlas connection string
    connection_string = "mongodb+srv://camping:SqP6B8wLx62DsUf6@cluster0.l5yaw7u.mongodb.net/TestCamping"

    try:
        # Connect to MongoDB Atlas using mongoengine
        connect(host=connection_string)

        print("Connection to MongoDB Atlas using mongoengine successful!")
    except Exception as e:
        print(f"Failed to connect to MongoDB Atlas using mongoengine: {e}")
        
if __name__ == "__main__":
    test_connection()
"""
#MONGODB_DATABASES = {"default": {"name": "django_mongoengine"}}
MONGODB_DATABASES = {
    "mydb": {
        "name": "TestCamping",
        "host": "cluster0.l5yaw7u.mongodb.net",
        "port": 27017,
        "username": "camping",
        "password": "SqP6B8wLx62DsUf6",
        "authentication_source": "admin",
        #"alias": "mydb",
    },
}

"""
USERNAME = env("USERNAME")
MONGODB_DATABASES = {
    "default": {
        "name": "TestCamping",
        "host": env("MONGODB_HOST"),
        "port": env("MONGODB_PORT"),
        "password": env("MONGODB_PASSWORD"),
        "username": env("MONGODB_USERNAME"),
        "tz_aware": True, # if you using timezones in django (USE_TZ = True)
    },
}

#PASSWORD = env("PASSWORD")
#HOST = env("HOST")
#mongoengine.connect(db="TestCamping", host=f"mongodb+srv://cluster0.l5yaw7u.mongodb.net/",
#                    username=USERNAME, password="SqP6B8wLx62DsUf6")
"""

#DATABASES = {"default": {"ENGINE": "django.db.backends.dummy"}}

# Application definition
 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #'rest_framework',
    'django_mongoengine',
    #'mongoengine.contrib.admin',
    'django_mongoengine.mongo_auth',
    #'django_mongoengine.mongo_admin',
    #"rest_framework.authtoken",
    #"django_filters",
    "camping",
    #"admin_honeypot",
    #"axes",   
]
 
#AUTH_USER_MODEL = 'mongo_auth.MongoUser'
 
#AUTHENTICATION_BACKENDS = ('mongoengine.django.auth.MongoEngineBackend',)
 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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



#SESSION_ENGINE='django_mongoengine.sessions'
#Not sur if this is correct or if it is necessary to use "django_mongoengine.sessions" instead
#as in the github of mongoengine
#SESSION_SERIALIZER = 'django_mongoengine.sessions.BSONSerializer'
#INSTALLED_APPS += ["django_mongoengine"]



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
 
AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)
 
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