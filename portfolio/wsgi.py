"""
WSGI config for portfolio project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# 운영 환경을 기본으로 사용 (Railway 등에서 사용)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings.prod')

application = get_wsgi_application()
