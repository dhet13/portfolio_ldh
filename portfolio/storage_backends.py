"""
Supabase Storage를 위한 커스텀 Django Storage Backend
Supabase Python SDK를 사용하여 파일 업로드/다운로드 처리
"""
from django.core.files.storage import Storage
from django.conf import settings
from django.utils.deconstruct import deconstructible
from supabase import create_client, Client
from io import BytesIO
import os
import mimetypes
from urllib.parse import urljoin


@deconstructible
class SupabaseStorage(Storage):
    """
    Supabase Storage를 위한 Django Storage Backend
    """

    def __init__(self):
        self.supabase_url = settings.SUPABASE_URL
        self.supabase_key = settings.SUPABASE_KEY
        self.bucket_name = settings.SUPABASE_BUCKET
        self.client: Client = create_client(self.supabase_url, self.supabase_key)

    def _get_storage_client(self):
        """Supabase Storage 클라이언트 반환"""
        return self.client.storage.from_(self.bucket_name)

    def _open(self, name, mode='rb'):
        """
        파일을 열어서 반환
        """
        try:
            storage = self._get_storage_client()
            # Supabase에서 파일 다운로드
            response = storage.download(name)
            return BytesIO(response)
        except Exception as e:
            raise IOError(f"파일을 열 수 없습니다: {name}. 에러: {str(e)}")

    def _save(self, name, content):
        """
        파일을 Supabase Storage에 저장
        """
        try:
            storage = self._get_storage_client()

            # content가 InMemoryUploadedFile이나 TemporaryUploadedFile인 경우
            if hasattr(content, 'read'):
                file_data = content.read()
            else:
                file_data = content

            # MIME 타입 추정
            content_type, _ = mimetypes.guess_type(name)
            if not content_type:
                content_type = 'application/octet-stream'

            # Supabase Storage에 업로드
            storage.upload(
                path=name,
                file=file_data,
                file_options={"content-type": content_type}
            )

            return name

        except Exception as e:
            raise IOError(f"파일 저장 실패: {name}. 에러: {str(e)}")

    def delete(self, name):
        """
        파일 삭제
        """
        try:
            storage = self._get_storage_client()
            storage.remove([name])
        except Exception as e:
            raise IOError(f"파일 삭제 실패: {name}. 에러: {str(e)}")

    def exists(self, name):
        """
        파일 존재 여부 확인
        """
        try:
            storage = self._get_storage_client()
            # list 메서드로 파일 존재 확인
            files = storage.list(path=os.path.dirname(name))
            filename = os.path.basename(name)
            return any(f['name'] == filename for f in files)
        except Exception:
            return False

    def listdir(self, path):
        """
        디렉토리 내 파일 목록 반환
        """
        try:
            storage = self._get_storage_client()
            files = storage.list(path=path)

            # 디렉토리와 파일 구분
            directories = []
            filenames = []

            for item in files:
                if item.get('id'):  # 파일
                    filenames.append(item['name'])
                else:  # 디렉토리
                    directories.append(item['name'])

            return directories, filenames
        except Exception as e:
            raise IOError(f"디렉토리 목록 가져오기 실패: {path}. 에러: {str(e)}")

    def size(self, name):
        """
        파일 크기 반환 (bytes)
        """
        try:
            storage = self._get_storage_client()
            files = storage.list(path=os.path.dirname(name))
            filename = os.path.basename(name)

            for f in files:
                if f['name'] == filename:
                    return f.get('metadata', {}).get('size', 0)

            return 0
        except Exception:
            return 0

    def url(self, name):
        """
        파일의 공개 URL 반환
        """
        # Public bucket의 경우 공개 URL 생성
        base_url = f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/"
        return urljoin(base_url, name)

    def get_accessed_time(self, name):
        """
        파일의 마지막 접근 시간 (Supabase는 지원하지 않음)
        """
        return None

    def get_created_time(self, name):
        """
        파일 생성 시간
        """
        try:
            storage = self._get_storage_client()
            files = storage.list(path=os.path.dirname(name))
            filename = os.path.basename(name)

            for f in files:
                if f['name'] == filename:
                    created_at = f.get('created_at')
                    if created_at:
                        from datetime import datetime
                        return datetime.fromisoformat(created_at.replace('Z', '+00:00'))

            return None
        except Exception:
            return None

    def get_modified_time(self, name):
        """
        파일 수정 시간
        """
        try:
            storage = self._get_storage_client()
            files = storage.list(path=os.path.dirname(name))
            filename = os.path.basename(name)

            for f in files:
                if f['name'] == filename:
                    updated_at = f.get('updated_at')
                    if updated_at:
                        from datetime import datetime
                        return datetime.fromisoformat(updated_at.replace('Z', '+00:00'))

            return None
        except Exception:
            return None
