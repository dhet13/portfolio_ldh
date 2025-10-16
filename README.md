# ai 포트폴리오 사이트

> **"채용 담당자가 5분 안에 제 역량을 파악할 수 있도록 설계했습니다"**

📌 **핵심 기능:**
- 프로젝트 히스토리 타임라인 (회사별 · 개인 프로젝트 구분)
- GitHub README 자동 임포트 + 마크다운 렌더링
- 우측 AI 어시스턴트 (경력 관련 실시간 Q&A)

🛠 **기술 스택:** Django 5.0 · PostgreSQL · Tailwind CSS · OpenAI API
🚀 **배포:** Railway (자동 배포 파이프라인)

---

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.0.6-green)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.1-06B6D4)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 목차

- [프로젝트 소개](#-프로젝트-소개)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 및 실행](#-설치-및-실행)
- [환경 변수 설정](#-환경-변수-설정)
- [배포](#-배포)
- [개발 가이드](#-개발-가이드)
- [라이선스](#-라이선스)

## 🎯 프로젝트 소개

Django 기반의 개인 포트폴리오 웹사이트입니다. 자기소개, 스킬셋, 경력, 프로젝트 소개 및 AI 채팅 기능을 포함하고 있습니다.

**주요 특징:**
- 🎨 TailwindCSS를 활용한 반응형 디자인
- 🤖 OpenAI/Google Gemini API 기반 AI 채팅
- 📦 Supabase Storage를 통한 미디어 파일 관리
- 🚀 Railway 플랫폼 배포 최적화
- 🔐 환경별 설정 분리 (dev/prod)

## ✨ 주요 기능

### 1. 포트폴리오 섹션
- **자기소개**: 프로필 정보 및 소개글
- **스킬셋**: 기술 스택 및 숙련도 표시
- **경력**: 회사 경력 및 담당 업무
- **프로젝트**: 프로젝트 카드 및 상세 모달

### 2. AI 채팅
- OpenAI GPT 또는 Google Gemini와 대화
- 우측 패널 형태의 인터페이스
- 대화 기록 저장 및 관리

### 3. 관리자 기능
- Django Admin을 통한 컨텐츠 관리
- 이미지 업로드 및 Supabase 동기화
- 커스텀 관리 명령어 제공

## 🛠 기술 스택

### Backend
- **Django 5.0.6**: 웹 프레임워크
- **PostgreSQL**: 데이터베이스 (Supabase)
- **Gunicorn**: WSGI 서버
- **WhiteNoise**: 정적 파일 서빙

### Frontend
- **TailwindCSS 4.1**: CSS 프레임워크
- **Django Templates**: 템플릿 엔진
- **Markdown**: 컨텐츠 렌더링

### Storage & Deployment
- **Supabase Storage**: 미디어 파일 저장소
- **Railway**: 호스팅 플랫폼
- **GitHub**: 버전 관리 및 CI/CD

### AI Integration
- **OpenAI API**: GPT 모델
- **Google Gemini API**: Gemini 모델

## 📁 프로젝트 구조

```
portfolio_ldh/
├── portfolio/              # Django 프로젝트 설정
│   ├── settings/          # 환경별 설정 (base, dev, prod)
│   ├── storage_backends.py # Supabase 커스텀 스토리지
│   ├── urls.py            # 메인 URL 라우팅
│   └── wsgi.py            # WSGI 설정
├── core/                  # 메인 앱 (프로필, 스킬, 경력)
│   ├── models.py          # Profile, Skill, Experience 모델
│   ├── views.py           # 뷰 함수
│   ├── management/        # 커스텀 관리 명령어
│   └── templates/         # 템플릿 파일
├── projects/              # 프로젝트 앱
│   ├── models.py          # Project, ProjectImage 모델
│   └── templates/         # 프로젝트 템플릿
├── ai_chat/               # AI 채팅 앱
│   ├── models.py          # Conversation, Message 모델
│   ├── services.py        # AI API 통합
│   └── views.py           # 채팅 뷰
├── templates/             # 전역 템플릿
│   ├── base.html          # 베이스 템플릿
│   └── partials/          # 재사용 가능한 컴포넌트
├── static/                # 정적 파일 (CSS, JS, images)
├── theme/                 # TailwindCSS 앱
├── requirements.txt       # Python 의존성
├── package.json           # Node.js 의존성
├── manage.py              # Django 관리 스크립트
├── .env.example           # 환경 변수 예제
├── railway.json           # Railway 배포 설정
└── DEPLOYMENT.md          # 배포 가이드
```

## 🚀 설치 및 실행

### 1. 사전 요구사항

- Python 3.12+
- Node.js 18+
- PostgreSQL (또는 Supabase 계정)
- Supabase Storage 버킷

### 2. 저장소 클론

```bash
git clone https://github.com/dhet13/portfolio_ldh.git
cd portfolio_ldh
```

### 3. Python 가상환경 설정

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 4. 의존성 설치

```bash
# Python 패키지 설치
pip install -r requirements.txt

# Node.js 패키지 설치
npm install
```

### 5. 환경 변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 필요한 값을 입력합니다:

```bash
cp .env.example .env
```

자세한 내용은 [환경 변수 설정](#-환경-변수-설정) 섹션을 참고하세요.

### 6. 데이터베이스 마이그레이션

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. 슈퍼유저 생성

```bash
python manage.py createsuperuser
```

### 8. 정적 파일 수집

```bash
python manage.py collectstatic --no-input
```

### 9. 개발 서버 실행

```bash
# 터미널 1: Django 서버
python manage.py runserver

# 터미널 2: TailwindCSS 빌드 (watch 모드)
npm run build:css
```

브라우저에서 `http://127.0.0.1:8000` 접속

## 🔐 환경 변수 설정

### 필수 환경 변수

```bash
# Django 설정
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@host:port/database

# Supabase Storage
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_BUCKET=portfolio-media
```

### 선택적 환경 변수

```bash
# AI 기능 (둘 중 하나 이상 필수)
OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-google-api-key

# 배포 환경 (Railway 자동 설정)
RAILWAY_ENVIRONMENT=production
ALLOWED_HOSTS=your-domain.railway.app
```

### SECRET_KEY 생성

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📦 배포

### Railway 배포

1. **GitHub 레포지토리 연동**
   ```bash
   git push origin main
   ```

2. **Railway 프로젝트 생성**
   - [railway.app](https://railway.app) 로그인
   - "New Project" → "Deploy from GitHub repo" 선택

3. **환경 변수 설정**
   - Railway Dashboard → Variables 탭
   - 필수 환경 변수 입력 (위 섹션 참고)

4. **자동 배포**
   - main 브랜치 푸시 시 자동 배포
   - `railway.json` 설정에 따라 빌드/실행

자세한 배포 가이드는 [DEPLOYMENT.md](DEPLOYMENT.md)를 참고하세요.

## 👨‍💻 개발 가이드

### 커스텀 관리 명령어

```bash
# 슈퍼유저 자동 생성 (개발용)
python manage.py createsu

# 로컬 미디어 파일을 Supabase에 업로드
python manage.py upload_local_media

# DB와 Supabase Storage 동기화
python manage.py sync_db_with_supabase

# Supabase 파일 목록 조회
python manage.py list_supabase_files

# 이미지 경로 수정
python manage.py fix_image_paths

# Storage 연결 테스트
python manage.py test_storage
```

### 코드 품질 도구

```bash
# Black: 코드 포맷팅
black .

# isort: import 정렬
isort .

# flake8: 린팅
flake8 .
```

### TailwindCSS 빌드

```bash
# Watch 모드 (개발 시)
npm run build:css

# 프로덕션 빌드
npx tailwindcss -i ./styles/globals.css -o ./portfolio/static/css/main.css --minify
```

### 템플릿 구조

```django
{# templates/base.html - 베이스 템플릿 #}
{% extends "base.html" %}

{# 공통 파셜 사용 #}
{% include "partials/header.html" %}
{% include "partials/footer.html" %}

{# 앱별 템플릿 상속 #}
{% block content %}
  {# 페이지 내용 #}
{% endblock %}
```

### 모델 변경 워크플로우

```bash
# 1. models.py 수정
# 2. 마이그레이션 파일 생성
python manage.py makemigrations

# 3. 마이그레이션 적용
python manage.py migrate

# 4. (선택) 마이그레이션 확인
python manage.py showmigrations
```

## 🧪 테스트

```bash
# 전체 테스트 실행
python manage.py test

# 특정 앱 테스트
python manage.py test core
python manage.py test projects
python manage.py test ai_chat

# 커버리지 측정
coverage run --source='.' manage.py test
coverage report
```

## 🐛 트러블슈팅

### 정적 파일이 로드되지 않을 때

```bash
python manage.py collectstatic --clear --no-input
```

### 데이터베이스 연결 오류

- `DATABASE_URL` 환경 변수 확인
- PostgreSQL 서버 실행 상태 확인
- Supabase 프로젝트 활성화 확인

### Supabase Storage 업로드 실패

- `SUPABASE_URL`, `SUPABASE_KEY` 환경 변수 확인
- Supabase 버킷이 생성되어 있는지 확인
- 버킷 권한 설정 확인 (public 읽기 권한)

### TailwindCSS 스타일이 적용되지 않을 때

```bash
# TailwindCSS 재빌드
npm run build:css

# 캐시 삭제
python manage.py collectstatic --clear
```

## 📚 참고 자료

- [Django 공식 문서](https://docs.djangoproject.com/)
- [TailwindCSS 문서](https://tailwindcss.com/docs)
- [Supabase 문서](https://supabase.com/docs)
- [Railway 문서](https://docs.railway.app/)
- [OpenAI API 문서](https://platform.openai.com/docs)

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 👤 작성자

**이동한 (Lee Dong Han)**

- GitHub: [@dhet13](https://github.com/dhet13)
- Repository: [portfolio_ldh](https://github.com/dhet13/portfolio_ldh)

## 🙏 기여

이슈 및 풀 리퀘스트는 언제든 환영합니다!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**⭐ 이 프로젝트가 도움이 되었다면 스타를 눌러주세요!**
