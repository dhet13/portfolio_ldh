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
        import io
        import logging
        import uuid
        import os

        logger = logging.getLogger(__name__)

        content.seek(0)
        ext = os.path.splitext(name)[1].lower()
        unique_name = f"{uuid.uuid4().hex}{ext}"

        directory = os.path.dirname(name)
        full_path = os.path.join(directory, unique_name).replace('\\', '/') if directory else unique_name

        file_data = content.read()
        file_obj = io.BytesIO(file_data)

        try:
            res = self.client.storage.from_(self.bucket).upload(
                path=full_path,
                file=file_obj,
                file_options={"upsert": True}
            )
        except Exception as e:
            logger.exception("Supabase upload exception for %s: %s", full_path, e)
            raise

        # supabase-py v1 did not have a dedicated error class, check for dict response
        if (isinstance(res, dict) and res.get("error")):
            logger.error("Upload failed for %s: %s", full_path, res)
            raise Exception(f"Upload failed: {res}")

        # Verification step
        try:
            items = self.client.storage.from_(self.bucket).list(path=os.path.dirname(full_path) or '')
            if not any(item['name'] == os.path.basename(full_path) for item in items):
                logger.error("Uploaded file not found in list after upload: %s", full_path)
                raise Exception("Upload reported success but file not found")
        except Exception as e:
            logger.exception("Error verifying uploaded file: %s", e)
            # Depending on policy, you might want to raise the exception
            # or just log the verification failure and continue.
            raise

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