"""
Supabase Storage를 위한 커스텀 Django Storage Backend
Supabase Python SDK를 사용하여 파일 업로드/다운로드 처리
"""
from django.core.files.storage import Storage
from django.conf import settings
from django.utils.deconstruct import deconstructible
from django.utils.encoding import filepath_to_uri
from supabase import create_client, Client
from io import BytesIO
import os
import mimetypes
import uuid
from datetime import datetime
from urllib.parse import urljoin, quote


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

    def _sanitize_filename(self, name):
        """
        한글 및 특수문자 파일명을 안전한 ASCII 파일명으로 변환
        예: test/한글파일.jpg -> test/20250113_a1b2c3d4.jpg
        """
        # 디렉토리와 파일명 분리
        directory = os.path.dirname(name)
        filename = os.path.basename(name)

        # 파일명과 확장자 분리
        name_part, ext = os.path.splitext(filename)

        # ASCII가 아닌 문자가 있는지 확인
        try:
            name_part.encode('ascii')
            # ASCII만 있으면 원본 파일명 유지
            has_non_ascii = False
        except UnicodeEncodeError:
            has_non_ascii = True

        # 한글이나 특수문자가 있으면 타임스탬프 + UUID로 변환
        if has_non_ascii:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = uuid.uuid4().hex[:8]
            safe_filename = f"{timestamp}_{unique_id}{ext}"
        else:
            safe_filename = filename

        # 디렉토리와 결합
        if directory:
            return os.path.join(directory, safe_filename).replace('\\', '/')
        return safe_filename

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
        한글 파일명은 자동으로 안전한 ASCII 파일명으로 변환됩니다.
        """
        try:
            storage = self._get_storage_client()

            # 한글 파일명을 안전한 파일명으로 변환
            safe_name = self._sanitize_filename(name)

            # content가 InMemoryUploadedFile이나 TemporaryUploadedFile인 경우
            if hasattr(content, 'read'):
                file_data = content.read()
            else:
                file_data = content

            # MIME 타입 추정 (원본 파일명 기준)
            content_type, _ = mimetypes.guess_type(name)
            if not content_type:
                content_type = 'application/octet-stream'

            # Supabase Storage에 업로드 (변환된 파일명 사용)
            storage.upload(
                path=safe_name,
                file=file_data,
                file_options={"content-type": content_type}
            )

            # 변환된 파일명 반환 (Django가 DB에 저장할 경로)
            return safe_name

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
        파일의 공개 URL 반환 (한글 파일명 지원)
        """
        # 한글 파일명을 URL 인코딩
        encoded_name = quote(name, safe='/')
        # Public bucket의 경우 공개 URL 생성
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{encoded_name}"

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
