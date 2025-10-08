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
        self.client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket = settings.SUPABASE_BUCKET

    def _save(self, name, content):
        # 파일 업로드 로직
        # Supabase Storage 파일업로드
        
        # get_valid_filename(name)으로 안전한 파일명 생성
        safe_name = get_valid_filename(name)

        # content.read()로 바이트 데이터 읽기
        file_data = content.read()

        # self.client.storage.from_(self.bucket).upload() 호출
        self.client.storage.from_(self.bucket).upload(
            path=safe_name,
            file=file_data,
            file_options={"upsert": "true"}
        )

        # 업로드한 경로 (path) 변환
        return safe_name

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
        return f"{base_url}/storage/v1/object/public/{self.bucket}/{quote(name, safe='')}"

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