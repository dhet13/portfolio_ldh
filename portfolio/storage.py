import uuid
import os
from io import BytesIO
from django.core.files.storage import Storage
from django.core.files.base import File
from django.utils.text import get_valid_filename
from supabase import create_client
from django.conf import settings
from datetime import datetime
from urllib.parse import quote

class SupabaseStorage(Storage):
    def __init__(self):
        # Supabase 클라이언트 초기화
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise ValueError(
                "Supabase configuration is missing. "
                "Please set SUPABASE_URL and SUPABASE_KEY environment variables."
            )

        self.client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket = settings.SUPABASE_BUCKET

    def _save(self, name, content):
        from io import BytesIO

        # 파일 포인터를 처음으로 되돌립니다.
        content.seek(0)

        # 파일 확장자 추출
        ext = os.path.splitext(name)[1].lower()

        # UUID로 고유한 파일명 생성
        unique_name = f"{uuid.uuid4().hex}{ext}"

        # 디렉토리 경로 유지
        directory = os.path.dirname(name)
        if directory:
            full_path = os.path.join(directory, unique_name).replace('\\', '/')
        else:
            full_path = unique_name

        # 파일을 청크 단위로 안전하게 읽어 메모리 버퍼에 씁니다.
        file_buffer = BytesIO()
        for chunk in content.chunks():
            file_buffer.write(chunk)
        file_buffer.seek(0)
        file_data = file_buffer.getvalue()

        # Supabase에 업로드
        self.client.storage.from_(self.bucket).upload(
            path=full_path,
            file=file_data,
            file_options={"upsert": "true"}
        )

        # 업로드된 최종 경로 반환
        return full_path

    def _open(self, name, mode='rb'):
        # Supabase에서 파일 다운로드하여 파일 객체 반환
        try:
            data = self.client.storage.from_(self.bucket).download(name)
            return File(BytesIO(data), name=name)
        except Exception:
            raise FileNotFoundError(f"File {name} not found in Supabase Storage")

    def url(self, name):
        # Supabase Public URL 생성
        # 형식: https://{project}.supabase.co/storage/v1/object/public/{bucket}/{path}
        base_url = settings.SUPABASE_URL  # https://rpbjeztxfmzneeoqlatn.supabase.co
        # UUID 파일명은 이미 안전하므로 quote 불필요
        return f"{base_url}/storage/v1/object/public/{self.bucket}/{name}"

    def exists(self, name):
        #파일 존재 여부 확인
        try:
            folder, filename = os.path.split(name)
            files = self.client.storage.from_(self.bucket).list(path=folder or '')
            return any(f['name'] == filename for f in files)
        
        except Exception:
            return False


    def delete(self, name):
        # Supabase Storage에서 파일 삭제
        try:
            self.client.storage.from_(self.bucket).remove([name])
        except Exception:
            # 이미 삭제된 파일이거나 에러 발생 시 무시
            pass