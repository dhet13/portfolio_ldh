"""
Django base settings for portfolio project.
이 파일은 모든 환경(dev, prod)에서 공통으로 사용되는 설정을 포함합니다.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path
from decouple import config
import dj_database_url

import os
from dotenv import load_dotenv
from django.conf import settings
import openai

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# settings 패키지로 이동했으므로 parent.parent.parent로 수정
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-key-change-this-in-production')

# DEBUG and ALLOWED_HOSTS are set in dev.py and prod.py
# Railway-specific settings are in prod.py


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    'core',
    'ai_chat',
    'projects',
]

# django_browser_reload는 dev.py에서 추가됩니다

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# BrowserReloadMiddleware는 dev.py에서 추가됩니다

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',  # 프로젝트 루트 레벨 템플릿 (공용)
            BASE_DIR / 'portfolio' / 'templates',  # portfolio 앱 템플릿
        ],
        'APP_DIRS': True,  # 각 앱의 templates 디렉토리도 자동 탐색
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Supabase Storage 설정 (커스텀 백엔드 사용)
# ------------------------------------------------------------------------------
# 참고: 이 설정을 위해 Railway 환경 변수에 다음이 필요합니다:
# SUPABASE_URL: Supabase 프로젝트 URL (예: https://xxxxx.supabase.co)
# SUPABASE_KEY: Supabase의 service_role 키 (Settings > API > service_role key)
# SUPABASE_BUCKET: 'portfolio-media' (버킷명)

# Supabase 설정
SUPABASE_URL = config('SUPABASE_URL', default='')
SUPABASE_KEY = config('SUPABASE_KEY', default='')
SUPABASE_BUCKET = config('SUPABASE_BUCKET', default='portfolio-media')

# 커스텀 Supabase Storage Backend 사용
DEFAULT_FILE_STORAGE = 'portfolio.storage_backends.SupabaseStorage'

# MEDIA_URL 설정 - Supabase 공개 URL 구조
SUPABASE_PROJECT_ID = SUPABASE_URL.replace('https://', '').replace('.supabase.co', '') if SUPABASE_URL else ''
MEDIA_URL = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/"


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'portfolio' / 'static'
]

# WhiteNoise 설정은 prod.py에서 설정됩니다


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Django-Tailwind Settings
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]