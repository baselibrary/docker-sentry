# This file is just Python, with a touch of Django which means
# you can inherit and tweak settings to your hearts content.
from sentry.conf.server import *

import os.path

CONF_ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE':   os.environ.get('SENTRY_DB_ENGINE', 'django.db.backends.sqlite3'),
        'HOST':     os.environ.get('SENTRY_DB_HOST',   ''),
        'PORT':     os.environ.get('SENTRY_DB_PORT',   ''),
        'NAME':     os.environ.get('SENTRY_DB_NAME',   '/sentry/sentry.db'),
        'USER':     os.environ.get('SENTRY_DB_USER',   'postgres'),
        'PASSWORD': os.environ.get('SENTRY_DB_PASS',   ''),
    }
}

# You should not change this setting after your database has been created
# unless you have altered all schemas first
SENTRY_USE_BIG_INTS = True

# If you're expecting any kind of real traffic on Sentry, we highly recommend
# configuring the CACHES and Redis settings



# The administrative email for this installation.
# Note: This will be reported back to getsentry.com as the point of contact. See
# the beacon documentation for more information. This **must** be a string.
SENTRY_ADMIN_EMAIL = os.environ.get('SENTRY_ADMIN_EMAIL', '')

# Instruct Sentry that this install intends to be run by a single organization
# and thus various UI optimizations should be enabled.
SENTRY_SINGLE_ORGANIZATION = True

# Should Sentry allow users to create new accounts?
SENTRY_FEATURES['auth:register'] = False

#########
# Redis #
#########
REDIS_HOST = os.environ.get('SENTRY_REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.environ.get('SENTRY_REDIS_PORT', '6379')
REDIS_DB   = os.environ.get('SENTRY_REDIS_DB', '0')

# Generic Redis configuration used as defaults for various things including:
# Buffers, Quotas, TSDB

SENTRY_REDIS_OPTIONS = {
    'hosts': {
        0: {
            'host': REDIS_HOST,
            'port': REDIS_PORT,
            'db':   REDIS_DB
        }
    }
}

#########
# Cache #
#########

CACHE_TYPE = os.environ.get('SENTRY_CACHE_TYPE', 'redis')

if CACHE_TYPE == 'memcached':
    CACHES = {
        'default': {
             'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
             'LOCATION': ['127.0.0.1:11211'],
        }
    }
    SENTRY_CACHE = 'sentry.cache.django.DjangoCache'
else:
    SENTRY_CACHE = 'sentry.cache.redis.RedisCache'

#########
# Queue #
#########

# See https://docs.getsentry.com/on-premise/server/queue/ for more
# information on configuring your queue broker and workers. Sentry relies
# on a Python framework called Celery to manage queues.

CELERY_ALWAYS_EAGER = False
BROKER_URL = 'redis://%s:%s/%s' % (REDIS_HOST, REDIS_PORT, REDIS_DB)

###############
# Rate Limits #
###############

# Rate limits apply to notification handlers and are enforced per-project
# automatically.

SENTRY_RATELIMITER = 'sentry.ratelimits.redis.RedisRateLimiter'

##################
# Update Buffers #
##################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'

##########
# Quotas #
##########

# Quotas allow you to rate limit individual projects or the Sentry install as
# a whole.

SENTRY_QUOTAS = 'sentry.quotas.redis.RedisQuota'

########
# TSDB #
########

# The TSDB is used for building charts as well as making things like per-rate
# alerts possible.

SENTRY_TSDB = 'sentry.tsdb.redis.RedisTSDB'

################
# File storage #
################

# Any Django storage backend is compatible with Sentry. For more solutions see
# the django-storages package: https://django-storages.readthedocs.org/en/latest/

SENTRY_FILESTORE = 'django.core.files.storage.FileSystemStorage'
SENTRY_FILESTORE_OPTIONS = {
    'location': '/sentry/tmp/sentry-files',
}

##############
# Web Server #
##############

# You MUST configure the absolute URI root for Sentry:
SENTRY_URL_PREFIX = os.environ.get('SENTRY_SENTRY_URL_PREFIX', 'http://sentry.example.com') 

# If you're using a reverse proxy, you should enable the X-Forwarded-Proto
# header and uncomment the following settings
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SESSION_COOKIE_SECURE = True

SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    # 'workers': 3,  # the number of gunicorn workers
    # 'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
}

###############
# Mail Server #
###############

# For more information check Django's documentation:
#  https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = os.environ.get('SENTRY_EMAIL_HOST', 'localhost')
EMAIL_HOST_USER     = os.environ.get('SENTRY_EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('SENTRY_EMAIL_PASS', '')
EMAIL_PORT          = os.environ.get('SENTRY_EMAIL_PORT', '25')
EMAIL_USE_TLS       = bool(os.environ.get('SENTRY_EMAIL_USE_TLS', 'False'))

# The email address to send on behalf of
SERVER_EMAIL        = os.environ.get('SENTRY_SERVER_EMAIL', 'root@localhost')

# If you're using mailgun for inbound mail, set your API key and configure a
# route to forward to /api/hooks/mailgun/inbound/
MAILGUN_API_KEY     = os.environ.get('SENTRY_MAILGUN_API_KEY', '')

########
# etc. #
########

# If this file ever becomes compromised, it's important to regenerate your SECRET_KEY
# Changing this value will result in all current sessions being invalidated
SECRET_KEY = '5V1r7G3vQBr2gbU2tgDBNitmEuQ82JMtt7N0adHSx2IllzQhRK6HrA=='