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
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.sharepay.com.br',
    'www.sharepay.com.br',
    'sharepay.com.br',
    '.herokuapp.com',
    '.sharepaybill.herokuapp.com',
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
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.instagram',
    'adv_cache_tag',#Cached Tags
    'debug_toolbar',#Debug Toolbar
]
#Cached Tags
"""
So if you like the principle of a unique key for a given template for a given object/user or whatever, 
be sure to always use the same arguments, except the last one, and activate the ADV_CACHE_VERSIONING setting.
Note that we also manage an internal version number, which will always be compared to the cached one. 
This internal version number is only updated when the internal algorithm of django-adv-cache-tag changes. 
But you can update it to invalidate all cached templates by adding a ADV_CACHE_VERSION to your settings 
(our internal version and the value from this settings will be concatenated to get the internal version really used)
"""
ADV_CACHE_VERSIONING = True
"""
To add a primary key, simply set the ADV_CACHE_INCLUDE_PK setting to True, and the first argument (after the fragment’s name) will be used as a pk.
"""
ADV_CACHE_INCLUDE_PK = True
"""
The fragment name-->
The fragment name is the name to use as a base to create the cache key, and is defined just after the expiry time.
In django-adv-cache-tag, by setting ADV_CACHE_RESOLVE_NAME to True, a fragment name that is not quoted will be resolved as a variable that should be in the context.
"""
ADV_CACHE_RESOLVE_NAME= True

#Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
    '.sharepay.com.br',
    '.herokuapp.com',
    'www.sharepay.com.br',
    'sharepay.com.br',
]
#Cached Tags
"""
So if you like the principle of a unique key for a given template for a given object/user or whatever, 
be sure to always use the same arguments, except the last one, and activate the ADV_CACHE_VERSIONING setting.
Note that we also manage an internal version number, which will always be compared to the cached one. 
This internal version number is only updated when the internal algorithm of django-adv-cache-tag changes. 
But you can update it to invalidate all cached templates by adding a ADV_CACHE_VERSION to your settings 
(our internal version and the value from this settings will be concatenated to get the internal version really used)
"""
ADV_CACHE_VERSIONING = True
"""
To add a primary key, simply set the ADV_CACHE_INCLUDE_PK setting to True, and the first argument (after the fragment’s name) will be used as a pk.
"""
ADV_CACHE_INCLUDE_PK = True
"""
The fragment name-->
The fragment name is the name to use as a base to create the cache key, and is defined just after the expiry time.
In django-adv-cache-tag, by setting ADV_CACHE_RESOLVE_NAME to True, a fragment name that is not quoted will be resolved as a variable that should be in the context.
"""
ADV_CACHE_RESOLVE_NAME= True

#Debug Toolbar
# INTERNAL_IPS = [
#     '127.0.0.1',
#     '.sharepay.com.br',
#     '.herokuapp.com',
# ]

AUTH_USER_MODEL = 'users.CustomUser'

MIDDLEWARE = [
    #debug_toolbar MUST BE HERE below cache UPDATED
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    #Must be here on top
    # 'django.middleware.cache.UpdateCacheMiddleware',#This is to cache the entery page

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #Must be here on bottom
    # 'django.middleware.cache.FetchFromCacheMiddleware'#This is to cache the entery page
]
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_KEY_PREFIX = 'sharepay'

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
        'ENGINE': 'django.db.backends.mysql',
        # "LOCATION": [config('DATABASE_URL')],
        'NAME': 'sql_sharepay',
        'USER': 'sql_sharepay',
        'PASSWORD': 'SKcL4YnfyTibHp6L',
        'HOST': 'localhost',
        'PORT': '3306',
    }   
}

#Redis Cache
CACHE_TTL = 60 * 5
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_KEY_PREFIX = 'sharepay'
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [f"{config('REDIS_TLS_URL')}/1"],
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            "CONNECTION_POOL_KWARGS": {
                "ssl_cert_reqs": None,
                "max_connections": 500, 
                "retry_on_timeout": True
            },
        }
    }
}
"""
Django can by default use any cache backend as session backend and you benefit from that by using django-redis 
as backend for session storage without installing any additional backends:
"""
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

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
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SAMESITE = 'None'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    BASE_URL = "https://www.sharepay.com.br"

# CORS_REPLACE_HTTPS_REFERER      = False
# HOST_SCHEME                     = "http://"
# SECURE_HSTS_SECONDS             = None
# SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
# SECURE_FRAME_DENY               = False
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
LOGIN_URL = 'users:account_login'#if the user is not logged in, they redirect to login page

#django-allauth registraion settings
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS =1
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "optional" #Attention
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400 # 1 day
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'user']
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_SIGNUP_REDIRECT = LOGIN_REDIRECT_URL

# SOCIALACCOUNT
SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = False
SOCIALACCOUNT_AUTO_SIGNUP = False

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
    # 'facebook': {
    #     'METHOD': 'oauth2',
    #     'SDK_URL': '//connect.facebook.net/en_US/sdk.js',
    #     'SCOPE': ['email', 'public_profile'],
    #     'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
    #     'INIT_PARAMS': {'cookie': True},
    #     'FIELDS': [
    #         'id',
    #         'first_name',
    #         'last_name',
    #         'middle_name',
    #         'name',
    #         'name_format',
    #         # 'picture',
    #         'short_name',
    #         'birthday'
    #     ],
    #     'EXCHANGE_TOKEN': True,
    #     'LOCALE_FUNC': 'path.to.callable',
    #     'VERIFIED_EMAIL': False,
    #     'VERSION': 'v7.0',
    #     # 'LOCALE_FUNC': lambda request: 'en_US'
    # },
    # 'instagram': {
    #     'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
    #     'METHOD': 'oauth2',
    #     'LOCALE_FUNC': lambda request: 'en_US',
    #     'VERIFIED_EMAIL': False,
    # }
}

XCHANGE_TOKEN = True

#Google Settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('client_id_google')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('secret_google')

#Facebook Settings
# SOCIAL_AUTH_FACEBOOK_OAUTH2_KEY = config('client_id_facebook')
# SOCIAL_AUTH_FACEBOOK_OAUTH2_SECRET = config('secret_facebook')

#Instagram Settings
# PROFILE_URL = 'https://instagram.com/'
# SOCIAL_AUTH_INSTAGRAM_KEY = config('client_id_instagram')
# SOCIAL_AUTH_INSTAGRAM_SECRET = config('secret_instagram')
# SOCIAL_AUTH_INSTAGRAM_EXTRA_DATA = [('user', 'user')]


#Linkedin Settings
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = config('client_id_linkedin')
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = config('secret_linkedin')

# django_heroku.settings(locals())