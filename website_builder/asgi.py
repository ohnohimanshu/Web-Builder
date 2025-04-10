"""
ASGI config for website_builder project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_builder.settings')

application = get_asgi_application()
