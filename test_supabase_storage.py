"""
Supabase Storage S3 호환 API 연결 테스트 스크립트
"""
import os
import django
from pathlib import Path

# Django 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def test_storage_config():
    """스토리지 설정 확인"""
    print("=" * 60)
    print("📋 Django Storage 설정 확인")
    print("=" * 60)

    print(f"\n🔧 Storage Backend: {settings.DEFAULT_FILE_STORAGE}")
    print(f"🌐 Supabase URL: {settings.SUPABASE_URL}")
    print(f"🪣 Bucket: {settings.SUPABASE_BUCKET}")
    print(f"🔑 Service Role Key: {'*' * 20} (숨김)")
    print(f"🔗 Media URL: {settings.MEDIA_URL}")
    print()

def test_file_upload():
    """파일 업로드 테스트"""
    print("=" * 60)
    print("📤 파일 업로드 테스트")
    print("=" * 60)

    try:
        # 테스트 파일 생성
        test_content = "안녕하세요! Supabase Storage 테스트입니다."
        test_file_name = "test/test_upload.txt"

        print(f"\n업로드 시도 중: {test_file_name}")

        # 파일 업로드
        file_path = default_storage.save(
            test_file_name,
            ContentFile(test_content.encode('utf-8'))
        )

        print(f"✅ 업로드 성공!")
        print(f"📁 저장 경로: {file_path}")

        # URL 생성
        file_url = default_storage.url(file_path)
        print(f"🔗 파일 URL: {file_url}")

        # 파일 존재 확인
        exists = default_storage.exists(file_path)
        print(f"📂 파일 존재 확인: {exists}")

        # 파일 크기 확인
        size = default_storage.size(file_path)
        print(f"📏 파일 크기: {size} bytes")

        # 파일 삭제 (선택사항)
        print(f"\n🗑️  테스트 파일 삭제 중...")
        default_storage.delete(file_path)
        print(f"✅ 삭제 완료!")

        return True

    except Exception as e:
        print(f"\n❌ 에러 발생!")
        print(f"에러 타입: {type(e).__name__}")
        print(f"에러 메시지: {str(e)}")

        import traceback
        print("\n📋 전체 스택 트레이스:")
        print(traceback.format_exc())

        return False

if __name__ == "__main__":
    print("\n🚀 Supabase Storage 연결 테스트 시작\n")

    # 설정 확인
    test_storage_config()

    # 파일 업로드 테스트
    success = test_file_upload()

    print("\n" + "=" * 60)
    if success:
        print("✅ 모든 테스트 통과!")
    else:
        print("❌ 테스트 실패 - 위의 에러 메시지를 확인하세요.")
    print("=" * 60 + "\n")
