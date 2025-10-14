"""
Django development settings
로컬 개발 환경을 위한 설정
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# 개발 환경 전용 앱
INSTALLED_APPS += [
    'django_browser_reload',
]

# 개발 환경 전용 미들웨어
MIDDLEWARE += [
    'django_browser_reload.middleware.BrowserReloadMiddleware',
]

# Django-Tailwind 개발 설정
INTERNAL_IPS = [
    "127.0.0.1",
]

# 개발 환경에서는 SQLite 사용
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 정적 파일 설정 (개발 환경에서는 압축 없음)
# collectstatic 없이 runserver가 자동으로 정적 파일 제공
