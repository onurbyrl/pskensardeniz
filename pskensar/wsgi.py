"""
WSGI config for pskensar project.

It exposes the WSGI callable as a module-level variable named ``intervention``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pskensar.settings')

# NEVER FORGET # application olmalı
application = get_wsgi_application()
# intervention = get_wsgi_application()
