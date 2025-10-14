"""
ASGI config for portfolio project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# 운영 환경을 기본으로 사용 (Railway 등에서 사용)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings.prod')

application = get_asgi_application()
