"""
Django settings for sharepay project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import django_heroku
from pathlib import Path, os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'www.sharepay.app.br',
    'sharepay.app.br',
    'www.sharepay.com.br',
    'sharepay.com.br',
    'http://www.sharepay.com.br',
    'http://sharepay.com.br',
    'https://sharepaybill.herokuapp.com/',
    'https://git.heroku.com/sharepaybill.git'
    ]

# Application definition
INSTALLED_APPS = [
    #Django's Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    #Local Apps
    'users.apps.UsersConfig',
    'share.apps.ShareConfig',
    #Apps by others
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.linkedin_oauth2',
    'allauth.socialaccount.providers.facebook',
]

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sharepay.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'sharepay.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'decfeqioelq8iq',
        'USER': 'ohuwoglidavqod',
        'PASSWORD': '3e1684e449b1ef06f11168901c2b3e141a3fe086225c010d70c0bc3ce73be2b4',
        'HOST': 'ec2-52-213-119-221.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

""" Security Session """
# if not DEBUG:
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
BASE_URL = "https://www.sharepay.com.br"

# # PREPEND_WWW = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
MEDIA_ROOT  = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

#Settings SMTP email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST ='smtp.eu.mailgun.org'
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

#Settings API email
# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"  # or sendgrid.EmailBackend, or...
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')  # if you don't already have this in settings
SERVER_EMAIL = config('SERVER_EMAIL')  # ditto (default from-email for Django errors)

#AWS S3 Buckets Config
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
# https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#he response can be cached by browsers and intermediary caches for up to 1 day (60 seconds x 60 minutes x 24 hours)
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False
# AWS_S3_BUCKET_AUTH = False
# AWS_S3_GZIP = True
# AWS_IS_GZIPPED = True
AWS_S3_REGION_NAME = 'eu-west-1'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

"""A uthetications Redirects """
LOGOUT_REDIRECT_URL = 'share:index'#After login they goes to home page
LOGIN_REDIRECT_URL = 'share:index'#After login they goes to home page
LOGIN_URL = 'users:login'#if the user is not logged in, they redirect to login page

#django-allauth registraion settings
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional" #Attention
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5

# 1 day
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400

# ACCOUNT_EMAIL_SUBJECT_PREFIX
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None

#or any other page
ACCOUNT_LOGOUT_REDIRECT_URL ='users:account_login'

#Logout without confirmed page. risk aware <scripts> Inputs
ACCOUNT_LOGOUT_ON_GET = True

#Socials Accnout Redirects
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'share:index'
SOCIAL_AUTH_LOGIN_URL = 'users:account_login'

#ACCOUNT_FORMS
ACCOUNT_FORMS = {
    'login': 'users.forms.CustomLoginAccount',
    'signup': 'users.forms.CustomSignupAccount',
    'add_email': 'users.forms.CustomAddEmailAccount',
    'change_password': 'users.forms.ChangePasswordFormAccount',
    'set_password': 'users.forms.SetPasswordFormAccount',
    'reset_password': 'users.forms.ResetPasswordFormAccount',
    'reset_password_from_key': 'users.forms.ResetPasswordKeyFormAccount',
    'disconnect': 'users.forms.DisconnectFormAccount',
}

#SOCIALACCOUNT_FORMS
SOCIALACCOUNT_FORMS = {
    'disconnect': 'users.forms.DisconnectFormAccount',
    'signup': 'users.forms.SignupFormSocialAccount',
}

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # 'SCOPE': [
        #     'profile',
        #     'email',
        # ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'APP': {
            'client_id': config('client_id_google'),
            'secret': config('secret_google'),
            'key': ''
        }
    },
    'linkedin': {
        'SCOPE': [
            'r_basicprofile',
            'r_emailaddress'
        ],
        'PROFILE_FIELDS': [
            'id',
            'first-name',
            'last-name',
            'email-address',
            # 'picture-url',
            'public-profile-url',
        ],
        'HEADERS': {
            'x-li-src': 'msdk'
        },
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            # 'picture',
            'short_name'
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v7.0',
    }
}

XCHANGE_TOKEN = True

#Google Settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('client_id_google')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('secret_google')

#Facebook Settings
SOCIAL_AUTH_FACEBOOK_OAUTH2_KEY = config('client_id_facebook')
SOCIAL_AUTH_FACEBOOK_OAUTH2_SECRET = config('secret_facebook')

#Linkedin Settings
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = config('client_id_linkedin')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = config('secret_linkedin')

django_heroku.settings(locals())