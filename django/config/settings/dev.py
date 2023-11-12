from django.conf import settings
from split_settings.tools import include

from .base import *

if settings.DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    import socket  
    _,_, ips = socket.gethostbyname_ex(socket.gethostname())
    networks = ['.'.join(ip.split('.')[:-1]) for ip in ips]
    INTERNAL_IPS = [f'{net}.{ip}' for net in networks for ip in range(1,11) ]

    include(
        'components/logger.py'
    )

