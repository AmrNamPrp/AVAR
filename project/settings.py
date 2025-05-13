from pathlib import Path
from datetime import timedelta
import os
AUTH_USER_MODEL = 'account.CustomUser'

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-02%ebh5tra7!u^-l(*&a+^$nrzd36m$baf5@8fxs+fnjpe%zi8'
DEBUG = True
ALLOWED_HOSTS = ['192.168.1.111', '192.168.229.212','192.168.93.61','192.168.118.183','192.168.1.120','192.168.92.76','192.168.92.76','192.168.1.102','192.168.113.252','amrnamora.pythonanywhere.com','192.168.126.212','192.168.47.212',  '192.168.137.1','192.168.1.102', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'reservations',
    'django_filters',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
        'push_notifications',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = True  # For development only
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [

    'http://localhost:19006',
    'http://127.0.0.1:19006',
    'http://localhost:8082',  # Add Expo ports
    'http://192.168.1.102',  # Better IP pattern
    'http://192.168.137.1',  # Better IP pattern
    'http://192.168.47.212',  # Better IP pattern
    'http://192.168.126.212',  # Better IP pattern
    'https://amrnamora.pythonanywhere.com',  # Better IP pattern
    'http://192.168.191.212',  # Better IP pattern
    'http://192.168.1.102',  # Better IP pattern
    'http://192.168.95.9:8000',  # Better IP pattern
    'http://192.168.92.76:8000',  # Better IP pattern
    'http://192.168.137.1:8000',  # Better IP pattern
    'http://192.168.58.252:8000',  # Better IP pattern
    'http://192.168.113.252:8000',  # Better IP pattern
    'http://192.168.92.76:8000',  # Better IP pattern
    'http://192.168.1.120:8000',  # Better IP pattern
    'http://192.168.118.183:8000',
    'http://192.168.93.61:8000',
    'http://192.168.229.212:8000',
    'http://192.168.1.111:8000',

]
ROOT_URLCONF = 'project.urls'


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

WSGI_APPLICATION = 'project.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'REVE_NEW',
#         'USER': 'admin',
#         'PASSWORD': 'amr.186200420',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_CHARSET = 'utf-8'
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

#
# #######################
# from pathlib import Path
# from datetime import timedelta
# import os
# ####
# BASE_DIR = Path(__file__).resolve().parent.parent
#
# SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key')
# DEBUG = False
# ALLOWED_HOSTS = ['amrnamora.pythonanywhere.com']
#
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'account',
#     'reservations',
#     'django_filters',
#     'rest_framework',
#     'rest_framework_simplejwt.token_blacklist',
#     'corsheaders',
# ]
#
# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]
#
# # CORS Settings
# CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = [
#     'https://amrnamora.pythonanywhere.com',
#
# ]
# CSRF_TRUSTED_ORIGINS = [
#
#     'https://amrnamora.pythonanywhere.com',
# ]
# ROOT_URLCONF = 'project.urls'
#
#
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]
#
# WSGI_APPLICATION = 'project.wsgi.application'
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
#
# # REST Framework Settings
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_RENDERER_CLASSES': (
#         'rest_framework.renderers.JSONRenderer',
#     ),
# }
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=365),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'AUTH_HEADER_TYPES': ('Bearer',),
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',
# }
#
# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]
#
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True
# DEFAULT_CHARSET = 'utf-8'
# STATIC_ROOT='staticfiles'
# STATIC_URL = 'static/'
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
