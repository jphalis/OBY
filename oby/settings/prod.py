from oby.settings.common import *


# HOSTING + AUTHENTICATION
ADMINS = (
    ("JP", "halis@obystudio.com"),
)
MANAGERS = ADMINS
ALLOWED_HOSTS = [
    'www.obystudio.com',
    'obystudio.com',
    '*.obystudio.com',
    '127.0.0.1',
    '52.2.52.114',  # AWS Elastic IP
]
CORS_URLS_REGEX = r'^/hide/oby/api/.*$'


# S S L  S E C U R I T Y
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_SECONDS = 0
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_HOST = None
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False


# S T R I P E
STRIPE_SECRET_KEY = 'sk_live_6OlOtvEapbxPwcf1CZATzOXA'


# E M A I L
# Gmail
# EMAIL_HOST_USER = 'halis@obystudio.com'
# EMAIL_HOST_PASSWORD = '. Hockey18 .'


# P U S H  N O T I F I C A T I O N S
PUSH_NOTIFICATIONS_SETTINGS = {
    # "GCM_API_KEY": "<your api key>",
    # "GCM_POST_URL": "https://android.googleapis.com/gcm/send",
    # "GCM_MAX_RECIPIENTS": 1000,
    "APNS_HOST": "gateway.push.apple.com",
    "APNS_CERTIFICATE": os.path.join(os.path.dirname(BASE_DIR),
                                     'push_notifications',
                                     'certificates',
                                     'apns_prod.pem'),
    # "APNS_PORT": 2195
}


# A P P L I C A T I O N S
INSTALLED_APPS += (
    'storages',
)


# D A T A B A S E
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'oby_db_initial',
        'USER': 'obystudio',
        'PASSWORD': '84e52ccc-de80-4bc1-ae4c-5dd0934d42a6',
        'HOST': 'oby-dbs-virginia.cmyml5gujc5c.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
        # 'ATOMIC_REQUESTS': True,
    },
    'extra': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# T E M P L A T E S
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join('templates_simple')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
            # 'loaders': [
            #     ('django.template.loaders.cached.Loader', [
            #         'django.template.loaders.filesystem.Loader',
            #         'django.template.loaders.app_directories.Loader',
            #     ]),
            # ],
        },
    },
]


# H T M L  M I N I F I C A T I O N
KEEP_COMMENTS_ON_MINIFYING = False
EXCLUDE_FROM_MINIFYING = ('^hide/oby/admin/',)


# C A C H E
CACHES = {
    'default': {
        # 'BACKEND': 'oby.memcached.ElastiCache',
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': [
            'oby-memcached.il3181.cfg.use1.cache.amazonaws.com:11211',
            # '52.2.52.114:11211',
        ],
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 12
CACHE_MIDDLEWARE_KEY_PREFIX = ''


# S 3  B U C K E T
STATICFILES_DIRS = (
    os.path.join('oby', 'static_simple', 'static_dirs'),
    # '/Users/jphalis/Desktop/oby/src/oby/static/static_dirs/'
)
AWS_ACCESS_KEY_ID = 'AKIAJS5O4GAHA4MJH4NA'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'oby'
S3DIRECT_REGION = 'us-east-1'
AWS_CLOUDFRONT_DOMAIN = 'd2ragyhmhrkfg3.cloudfront.net'
STATICFILES_STORAGE = 'oby.s3utils.StaticRootS3BotoStorage'  # static files
STATIC_S3_PATH = 'media/'
DEFAULT_FILE_STORAGE = 'oby.s3utils.MediaRootS3BotoStorage'  # media uploads
DEFAULT_S3_PATH = 'static/'
S3_URL = '//{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)
# Without cloudfront
# MEDIA_URL = S3_URL + STATIC_S3_PATH
# STATIC_URL = S3_URL + DEFAULT_S3_PATH
MEDIA_ROOT = '/home/ubuntu/obystudio.com/oby/static_simple/media'
STATIC_ROOT = '/home/ubuntu/obystudio.com/oby/static_simple/static'
# With cloudfront
MEDIA_URL = '//{}/{}'.format(AWS_CLOUDFRONT_DOMAIN, STATIC_S3_PATH)
STATIC_URL = '//{}/{}'.format(AWS_CLOUDFRONT_DOMAIN, DEFAULT_S3_PATH)
# ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
AWS_FILE_EXPIRE = 200
AWS_PRELOAD_METADATA = True
# AWS_QUERYSTRING_AUTH = True
AWS_S3_SECURE_URLS = True
date_three_months_later = datetime.date.today() + datetime.timedelta(3 * 365 / 12)
expires = date_three_months_later.strftime('%A, %d %B %Y 20:00:00 EST')
AWS_HEADERS = {
    'Expires': expires,
    'Cache-Control': 'max-age=31536000',  # 365 days
}


# L O G G I N G
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'oby.settings.handlers.ThrottledAdminEmailHandler'
        # }
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
    },
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#     },
#     'formatters': {
#         'verbose': {
#             'format': (
#                 '%(asctime)s [%(process)d] [%(levelname)s] ' +
#                 'pathname=%(pathname)s lineno=%(lineno)s ' +
#                 'funcname=%(funcName)s %(message)s'),
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#         }
#     },
# }
