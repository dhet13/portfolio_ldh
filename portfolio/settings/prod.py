"""
Django production settings
운영 환경(Railway, 기타 배포 플랫폼)을 위한 설정
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Railway 배포 환경 지원
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')

if 'RAILWAY_ENVIRONMENT' in os.environ:
    RAILWAY_PUBLIC_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
    RAILWAY_PRIVATE_DOMAIN = os.environ.get('RAILWAY_PRIVATE_DOMAIN', '')

    if RAILWAY_PUBLIC_DOMAIN and RAILWAY_PUBLIC_DOMAIN not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)
    if RAILWAY_PRIVATE_DOMAIN and RAILWAY_PRIVATE_DOMAIN not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RAILWAY_PRIVATE_DOMAIN)

    # Railway 도메인 와일드카드 추가
    if '.railway.app' not in str(ALLOWED_HOSTS):
        ALLOWED_HOSTS.extend(['.railway.app', '.up.railway.app'])

# CSRF 설정
CSRF_TRUSTED_ORIGINS = []
if 'RAILWAY_ENVIRONMENT' in os.environ:
    # Railway 도메인을 CSRF trusted origins에 추가
    RAILWAY_PUBLIC_DOMAIN = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
    if RAILWAY_PUBLIC_DOMAIN:
        CSRF_TRUSTED_ORIGINS.append(f'https://{RAILWAY_PUBLIC_DOMAIN}')
    # Railway 도메인 패턴 추가
    CSRF_TRUSTED_ORIGINS.extend([
        'https://*.railway.app',
        'https://*.up.railway.app'
    ])

# 운영 환경 데이터베이스 (DATABASE_URL 환경 변수 사용)
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# WhiteNoise 정적 파일 압축 및 캐싱
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 보안 설정
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS 설정 (HTTPS Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1년
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
