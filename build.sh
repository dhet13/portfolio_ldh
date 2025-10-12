#!/usr/bin/env bash
# Railway 빌드 스크립트

set -o errexit

# 패키지 설치
pip3 install -r requirements.txt

# 정적 파일 수집
python3 manage.py collectstatic --no-input

# 마이그레이션 (선택사항 - 주의해서 사용)
# python3 manage.py migrate --no-input
