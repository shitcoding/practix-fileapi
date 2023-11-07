from django.conf import settings
from split_settings.tools import include

from .base import *

if settings.DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    INTERNAL_IPS = [
        '127.0.0.1',
    ]

    include(
        'components/logger.py'
    )

