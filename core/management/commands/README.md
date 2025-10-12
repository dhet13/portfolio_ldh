# Django Management Commands

## createsu - Create Superuser from Environment Variables

자동으로 superuser를 생성하는 명령어입니다. 주로 Railway, Heroku 등의 배포 환경에서 사용합니다.

### 사용법

```bash
python manage.py createsu
```

### 환경 변수

| 변수 | 필수 | 기본값 | 설명 |
|------|------|--------|------|
| `DJANGO_SUPERUSER_USERNAME` | 아니오 | `admin` | Superuser 사용자명 |
| `DJANGO_SUPERUSER_EMAIL` | 아니오 | `admin@example.com` | Superuser 이메일 |
| `DJANGO_SUPERUSER_PASSWORD` | **예** | - | Superuser 비밀번호 |

### Railway 배포 시 사용

Railway Variables 탭에 다음 환경 변수를 추가하세요:

```bash
DJANGO_SUPERUSER_USERNAME=your_admin_username
DJANGO_SUPERUSER_EMAIL=your_email@example.com
DJANGO_SUPERUSER_PASSWORD=your_secure_password
```

`build.sh`가 자동으로 배포 시 superuser를 생성합니다.

### 특징

- ✅ 이미 존재하는 사용자는 건너뜀 (에러 없음)
- ✅ 비대화형으로 실행 가능
- ✅ 배포 자동화에 적합
- ✅ 안전한 환경 변수 기반 인증

### 예제

```bash
# 로컬 개발
export DJANGO_SUPERUSER_USERNAME="admin"
export DJANGO_SUPERUSER_EMAIL="admin@localhost"
export DJANGO_SUPERUSER_PASSWORD="dev1234"
python manage.py createsu

# Railway CLI
railway run python manage.py createsu
```
