import os
import datetime
# import djcelery

from django.utils.translation import ugettext_lazy as _

# from celery.schedules import crontab
# from kombu import Exchange, Queue


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# HOSTING + AUTHENTICATION
SECRET_KEY = 'nl59wul4fep=2nk_e=nfe-frid9b)kqox#7sgh2wsws!x!e&^('
LOGIN_URL = "/signin/"
AUTH_USER_MODEL = 'accounts.MyUser'
MIN_PASSWORD_LENGTH = 5
FULL_DOMAIN_NAME = 'www.obystudio.com'


# E M A I L
# EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST = 'smtp.sendgrid.com'
EMAIL_HOST_USER = 'obyinc'
EMAIL_FROM = 'team@obystudio.com'
EMAIL_HOST_PASSWORD = '. Hockey18 .'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
EMAIL_TIMEOUT = None
"""
Testing:
python manage.py shell
exit()

Views:
from django.conf import settings
from django.core.mail import send_mail

send_mail('Subject', 'Message', 'from@example.com',
          ['to@example.com'], fail_silently=False)
"""
"""
If using gmail, you will need to
unlock Captcha to enable Django
to  send for you:
https://accounts.google.com/displayunlockcaptcha
"""


# I N T E R N A T I O N A L I Z A T I O N
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('af', _('Afrikaans')),
    ('ar', _('Arabic')),
    ('ast', _('Asturian')),
    ('az', _('Azerbaijani')),
    ('bg', _('Bulgarian')),
    ('be', _('Belarusian')),
    ('bn', _('Bengali')),
    ('br', _('Breton')),
    ('bs', _('Bosnian')),
    ('ca', _('Catalan')),
    ('cs', _('Czech')),
    ('cy', _('Welsh')),
    ('da', _('Danish')),
    ('de', _('German')),
    ('el', _('Greek')),
    ('en', _('English')),
    ('en-au', _('Australian English')),
    ('en-gb', _('British English')),
    ('eo', _('Esperanto')),
    ('es', _('Spanish')),
    ('es-ar', _('Argentinian Spanish')),
    ('es-mx', _('Mexican Spanish')),
    ('es-ni', _('Nicaraguan Spanish')),
    ('es-ve', _('Venezuelan Spanish')),
    ('et', _('Estonian')),
    ('eu', _('Basque')),
    ('fa', _('Persian')),
    ('fi', _('Finnish')),
    ('fr', _('French')),
    ('fy', _('Frisian')),
    ('ga', _('Irish')),
    ('gl', _('Galician')),
    ('he', _('Hebrew')),
    ('hi', _('Hindi')),
    ('hr', _('Croatian')),
    ('hu', _('Hungarian')),
    ('ia', _('Interlingua')),
    ('id', _('Indonesian')),
    ('io', _('Ido')),
    ('is', _('Icelandic')),
    ('it', _('Italian')),
    ('ja', _('Japanese')),
    ('ka', _('Georgian')),
    ('kk', _('Kazakh')),
    ('km', _('Khmer')),
    ('kn', _('Kannada')),
    ('ko', _('Korean')),
    ('lb', _('Luxembourgish')),
    ('lt', _('Lithuanian')),
    ('lv', _('Latvian')),
    ('mk', _('Macedonian')),
    ('ml', _('Malayalam')),
    ('mn', _('Mongolian')),
    ('mr', _('Marathi')),
    ('my', _('Burmese')),
    ('nb', _('Norwegian Bokmal')),
    ('ne', _('Nepali')),
    ('nl', _('Dutch')),
    ('nn', _('Norwegian Nynorsk')),
    ('os', _('Ossetic')),
    ('pa', _('Punjabi')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('pt-br', _('Brazilian Portuguese')),
    ('ro', _('Romanian')),
    ('ru', _('Russian')),
    ('sk', _('Slovak')),
    ('sl', _('Slovenian')),
    ('sq', _('Albanian')),
    ('sr', _('Serbian')),
    ('sr-latn', _('Serbian Latin')),
    ('sv', _('Swedish')),
    ('sw', _('Swahili')),
    ('ta', _('Tamil')),
    ('te', _('Telugu')),
    ('th', _('Thai')),
    ('tr', _('Turkish')),
    ('tt', _('Tatar')),
    ('udm', _('Udmurt')),
    ('uk', _('Ukrainian')),
    ('ur', _('Urdu')),
    ('vi', _('Vietnamese')),
    ('zh-hans', _('Simplified Chinese')),
    ('zh-hant', _('Traditional Chinese')),
]
LANGUAGES_BIDI = ["he", "ar", "fa", "ur"]
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','
USE_TZ = False


# A P P L I C A T I O N S
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'crispy_forms',
    'google_analytics',
    'rest_framework',
    'accounts',
    'analytics',
    'api',
    'comments',
    'contact',
    'core',
    'donations',
    'ecomm',
    'flag',
    'hashtags',
    'newsletter',
    'notifications',
    'photos',
    'push_notifications',
    'search',
    'shop',
    'widget_tweaks',
)


# M I D D L E W A R E
MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',  # Must be first
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
)


ROOT_URLCONF = 'oby.urls'
WSGI_APPLICATION = 'oby.wsgi.application'


# T E M P L A T E S
CRISPY_TEMPLATE_PACK = "bootstrap3"


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#         'OPTIONS': {
#             'min_length': 9,
#         },
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# S E S S I O N S
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 4 * 6  # six months
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'


# F I L E  U P L O A D S
FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5 MB


# A P I
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'SEARCH_PARAM': 'q',
}
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'core.utils.jwt_response_payload_handler',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=180),
    'JWT_ALLOW_REFRESH': False,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_SECRET_KEY': '%-23_#=hru4rl2m(lqax3viqz755qwnld+$sq1ddxpcdnt^5_g',
}


# R E W A R D S
DESERVES_REWARD_AMOUNT = 8
