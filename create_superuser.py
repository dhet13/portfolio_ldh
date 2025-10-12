#!/usr/bin/env python
"""
Standalone script to create a superuser.
Can be run directly on Railway via: railway run python create_superuser.py
"""
import os
import django

# Django 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# 환경 변수에서 읽기
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not password:
    print("❌ Error: DJANGO_SUPERUSER_PASSWORD environment variable is required")
    exit(1)

# 이미 존재하는지 확인
if User.objects.filter(username=username).exists():
    print(f"⚠️  User '{username}' already exists. Updating password...")
    user = User.objects.get(username=username)
    user.set_password(password)
    user.email = email
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"✅ Password updated for user '{username}'")
else:
    # 새로 생성
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✅ Superuser '{username}' created successfully!")

print(f"\n📝 Login credentials:")
print(f"   Username: {username}")
print(f"   Email: {email}")
print(f"   Password: {'*' * len(password)}")
