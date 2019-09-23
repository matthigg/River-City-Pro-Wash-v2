"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.1.11.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

SECRET_KEY = os.environ['RCPW_SECRET_KEY']

CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE              = True
SECURE_FRAME_DENY               = True
SECURE_CONTENT_TYPE_NOSNIFF     = True
SECURE_BROWSER_XSS_FILTER       = True
X_FRAME_OPTIONS                 = 'DENY'

# These settings prevent local production on Google Chrome 76
if os.environ['RCPW_LOCAL_HOST'] == 'None' or os.environ['RCPW_LOCAL_HOST_IP'] == 'None':
  SESSION_COOKIE_SECURE           = True  # prevents admin login on localhost
  SECURE_SSL_REDIRECT             = True  # requires SLL certificate in AWS
  SECURE_HSTS_PRELOAD             = True  # can really screw up local development
  SECURE_HSTS_INCLUDE_SUBDOMAINS  = True  
  SECURE_HSTS_SECONDS             = 60    # keep this low until 100% certain

DEBUG = os.environ['RCPW_DEBUG'] == '1'

ALLOWED_HOSTS = [
  'rivercityprowash.com',
  'www.rivercityprowash.com',
  'RiverCityProWashV2-env.ep9rnc2fhe.us-east-1.elasticbeanstalk.com',
]

if os.environ['RCPW_LOCAL_HOST'] == 'localhost':
  ALLOWED_HOSTS.append(os.environ['RCPW_LOCAL_HOST_IP'])
if os.environ['RCPW_LOCAL_HOST_IP'] == '127.0.0.1':
  ALLOWED_HOSTS.append(os.environ['RCPW_LOCAL_HOST_IP'])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'apps.contact_form',
    'apps.uploaded_images',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
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
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {

    # Sqlite3
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }

    # Postgres
    'default': {
      'ENGINE':   'django.db.backends.postgresql',
      'NAME':     os.environ['RCPW_DATABASE_NAME'],
      'USER':     os.environ['RCPW_DATABASE_USER'],
      'PASSWORD': os.environ['RCPW_DATABASE_PASSWORD'],
      'HOST':     os.environ['RCPW_DATABASE_HOST'],
      'PORT':     os.environ['RCPW_DATABASE_PORT'],
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Django's built-in message object that can be used to sent success messages,
# warnings, alerts, etc.
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
  os.path.join(BASE_DIR, 'local_static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# This will tell boto that when it uploads files to S3, it should set properties 
# on them so that when S3 serves them, it'll include some HTTP headers in the 
# response. Those HTTP headers, in turn, will tell browsers that they can cache 
# these files. The 'CacheControl' key:value pair takes precedence in most browers.
# https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=3600',
}

AWS_STORAGE_BUCKET_NAME = 'rcpw-eb-static-and-media-files'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_ACCESS_KEY_ID = os.environ['RCPW_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['RCPW_AWS_SECRET_ACCESS_KEY']
AWS_CLOUDFRONT_DOMAIN = 'dczid2jsu4h09.cloudfront.net'

# Tell django-storages the domain to use to refer to static files. You can choose
# between serving static files from an AWS S3 bucket or AWS Cloudfront - note 
# that Cloudfront typically takes 24 hours to update their cache unless you
# specifically invalidate a file or use object versioning. For quick changes,
# it's easier to use the S3 bucket.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_CUSTOM_DOMAIN = AWS_CLOUDFRONT_DOMAIN

# While using S3Boto3Storage this setting is supposed to allow static and media
# files (or whatever is stored in S3 via Boto3) to inherit the bucket's ACL, or
# "Access Control List", which is basically the read/write security settings for
# an AWS S3 bucket.
AWS_DEFAULT_ACL = None

# Tell the staticfiles app to use S3Boto3 storage when writing the collected 
# static files (when you run `collectstatic`). This setting is used during
# initial testing -- the S3Boto3Storage class is later subclassed by two custom
# classes in the custom_storages.py file, located in the root directory (the same
# directory as manage.py).
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Use custom storage classes for both static and media file storage by 
# subclassing S3Boto3Storage. This creates 2 subdirectories in the S3 bucket and
# conveniently separates static & media files
# https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/

STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'