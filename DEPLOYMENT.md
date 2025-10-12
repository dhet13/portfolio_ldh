# Railway 배포 가이드

## 📋 사전 준비

### 1. GitHub 레포지토리 준비
```bash
git init
git add .
git commit -m "Initial commit: Railway 배포 준비"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. Railway 계정 생성
- [railway.app](https://railway.app) 접속
- GitHub 계정으로 로그인

## 🚀 배포 단계

### Step 1: 새 프로젝트 생성
1. Railway 대시보드에서 **"New Project"** 클릭
2. **"Deploy from GitHub repo"** 선택
3. 포트폴리오 레포지토리 선택
4. Railway가 자동으로 감지하고 배포 시작

### Step 2: 환경 변수 설정
프로젝트 → **Variables** 탭에서 다음 환경 변수 추가:

#### ✅ 필수 환경 변수:
```bash
# Django 설정 (필수)
SECRET_KEY=<새로운-랜덤-시크릿-키>
DATABASE_URL=<your-supabase-or-railway-postgres-url>
DEBUG=False

# Supabase Storage (필수)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=<your-supabase-anon-key>
SUPABASE_BUCKET=portfolio-media
```

#### 🔑 선택적 환경 변수:
```bash
# ALLOWED_HOSTS는 자동 감지되므로 설정 불필요 (Railway 도메인 자동 추가)

# AI 기능이 필요한 경우
OPENAI_API_KEY=<your-openai-api-key>
GOOGLE_API_KEY=<your-google-api-key>
```

**💡 SECRET_KEY 생성 방법:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**⚠️ 중요:**
- `DATABASE_URL`은 Supabase PostgreSQL URL 또는 Railway Postgres 사용
- `SUPABASE_URL`과 `SUPABASE_KEY`는 미디어 파일 저장에 필요
- 모든 환경 변수는 Railway에서만 설정 (코드에 포함 금지)

### Step 3: 도메인 확인
1. Railway 프로젝트 → **Settings** 탭
2. **Generate Domain** 클릭하여 도메인 생성
3. 생성된 도메인을 `ALLOWED_HOSTS` 환경 변수에 추가

예: `your-app.up.railway.app`

### Step 4: 초기 설정 (선택사항)
배포 후 Railway 터미널에서 실행:

```bash
# 슈퍼유저 생성
python manage.py createsuperuser

# 마이그레이션 확인
python manage.py showmigrations
```

## ✅ 배포 확인

1. **Railway 로그 확인**
   - Deployments 탭에서 빌드 로그 확인
   - 에러가 없는지 체크

2. **사이트 접속**
   - 생성된 도메인으로 접속
   - 정적 파일(CSS/JS)이 정상 로드되는지 확인

3. **Admin 접속**
   - `https://<your-domain>/admin` 접속
   - 로그인 가능한지 확인

## 🔄 업데이트 배포

GitHub에 푸시하면 자동으로 재배포됩니다:

```bash
git add .
git commit -m "Update: 기능 추가"
git push origin main
```

## 🔧 트러블슈팅

### 정적 파일이 로드되지 않는 경우
```bash
# Railway 터미널에서 실행
python manage.py collectstatic --no-input
```

### 데이터베이스 연결 실패
- `DATABASE_URL` 환경 변수 확인
- Supabase 연결 문자열이 올바른지 체크
- Supabase 대시보드에서 IP 허용 확인

### 500 에러 발생
- `DEBUG=False` 상태에서 에러 로그 확인
- Railway 로그에서 상세 에러 메시지 확인
- `ALLOWED_HOSTS`에 도메인이 포함되어 있는지 확인

## 💡 추천 설정

### 커스텀 도메인 연결
1. Railway Settings → **Domains**
2. **Custom Domain** 클릭
3. 도메인 입력 및 DNS 설정
4. `ALLOWED_HOSTS`에 커스텀 도메인 추가

### 모니터링
- Railway Dashboard에서 메트릭 확인
- 메모리/CPU 사용량 모니터링
- 로그 정기적으로 확인

### 백업
- Supabase에서 자동 백업 활성화
- 중요한 데이터는 정기적으로 Export

## 📚 참고 자료

- [Railway 공식 문서](https://docs.railway.app)
- [Django 배포 체크리스트](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Supabase 문서](https://supabase.com/docs)

---

배포 중 문제가 발생하면 Railway 로그를 확인하거나 커뮤니티에 질문하세요!
