"""
한글 파일명 업로드 테스트
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def test_korean_filename():
    print("=" * 60)
    print("🇰🇷 한글 파일명 업로드 테스트")
    print("=" * 60)

    test_files = [
        ("test/한글파일.txt", "한글 파일명 테스트입니다."),
        ("test/프로젝트_문서.txt", "프로젝트 관련 문서"),
        ("test/이미지_설명.txt", "이미지 설명 파일"),
    ]

    success_count = 0
    fail_count = 0

    for filename, content in test_files:
        print(f"\n📤 업로드 시도: {filename}")
        try:
            # 파일 업로드
            saved_path = default_storage.save(
                filename,
                ContentFile(content.encode('utf-8'))
            )

            print(f"  ✅ 업로드 성공!")
            print(f"  📁 저장 경로: {saved_path}")

            # URL 생성
            file_url = default_storage.url(saved_path)
            print(f"  🔗 파일 URL: {file_url}")

            # 파일 존재 확인
            exists = default_storage.exists(saved_path)
            print(f"  📂 존재 확인: {exists}")

            # 파일 삭제
            default_storage.delete(saved_path)
            print(f"  🗑️  삭제 완료")

            success_count += 1

        except Exception as e:
            print(f"  ❌ 실패: {str(e)}")
            fail_count += 1

    print("\n" + "=" * 60)
    print(f"결과: 성공 {success_count}/{len(test_files)}, 실패 {fail_count}/{len(test_files)}")

    if fail_count == 0:
        print("✅ 모든 한글 파일명 테스트 통과!")
    else:
        print("⚠️  일부 테스트 실패")
    print("=" * 60)

if __name__ == "__main__":
    test_korean_filename()
