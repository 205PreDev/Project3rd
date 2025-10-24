"""
Local File Storage Service
개발 환경에서 Supabase 대신 로컬 파일 시스템 사용
"""
import os
import aiofiles
from pathlib import Path
from datetime import datetime
from typing import Optional
from fastapi import UploadFile, HTTPException


class LocalStorageService:
    """로컬 파일 시스템을 사용한 파일 저장 서비스"""

    def __init__(self, base_dir: str = "./uploads"):
        """
        Initialize local storage service

        Args:
            base_dir: 파일 저장 기본 디렉토리
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload_file(
        self,
        file: UploadFile,
        user_id: Optional[str] = None,
        folder: str = "trial"
    ) -> str:
        """
        파일을 로컬에 저장하고 경로 반환

        Args:
            file: 업로드된 파일
            user_id: 사용자 ID (없으면 session_id 사용)
            folder: 저장 폴더명

        Returns:
            저장된 파일의 상대 경로
        """
        try:
            # 디렉토리 구조: uploads/{folder}/{user_id or 'trial'}/
            user_folder = user_id if user_id else "anonymous"
            save_dir = self.base_dir / folder / user_folder
            save_dir.mkdir(parents=True, exist_ok=True)

            # 파일명 생성 (타임스탬프 + 원본 파일명)
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_ext = os.path.splitext(file.filename)[1]
            filename = f"{timestamp}_{file.filename}"
            file_path = save_dir / filename

            # 파일 저장
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)

            # 상대 경로 반환 (API에서 제공할 경로)
            relative_path = f"{folder}/{user_folder}/{filename}"
            return relative_path

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save file: {str(e)}"
            )

    async def save_bytes(
        self,
        content: bytes,
        filename: str,
        user_id: Optional[str] = None,
        folder: str = "processed"
    ) -> str:
        """
        바이트 데이터를 파일로 저장

        Args:
            content: 파일 내용 (bytes)
            filename: 파일명
            user_id: 사용자 ID
            folder: 저장 폴더명

        Returns:
            저장된 파일의 상대 경로
        """
        try:
            user_folder = user_id if user_id else "anonymous"
            save_dir = self.base_dir / folder / user_folder
            save_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename_with_time = f"{timestamp}_{filename}"
            file_path = save_dir / filename_with_time

            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)

            relative_path = f"{folder}/{user_folder}/{filename_with_time}"
            return relative_path

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save bytes: {str(e)}"
            )

    async def read_file(self, file_path: str) -> bytes:
        """
        파일 읽기

        Args:
            file_path: 파일 상대 경로

        Returns:
            파일 내용 (bytes)
        """
        try:
            full_path = self.base_dir / file_path

            if not full_path.exists():
                raise HTTPException(status_code=404, detail="File not found")

            async with aiofiles.open(full_path, 'rb') as f:
                content = await f.read()

            return content

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to read file: {str(e)}"
            )

    def get_file_url(self, file_path: str, base_url: str = "http://localhost:8000") -> str:
        """
        파일의 공개 URL 생성

        Args:
            file_path: 파일 상대 경로
            base_url: API 서버 베이스 URL

        Returns:
            파일 접근 URL
        """
        return f"{base_url}/files/{file_path}"

    async def delete_file(self, file_path: str) -> bool:
        """
        파일 삭제

        Args:
            file_path: 파일 상대 경로

        Returns:
            삭제 성공 여부
        """
        try:
            full_path = self.base_dir / file_path

            if full_path.exists():
                full_path.unlink()
                return True
            return False

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete file: {str(e)}"
            )


# Singleton instance
_local_storage = None


def get_local_storage() -> LocalStorageService:
    """Get or create LocalStorageService singleton"""
    global _local_storage
    if _local_storage is None:
        _local_storage = LocalStorageService()
    return _local_storage
