import os
from typing import BinaryIO
from datetime import datetime
from fastapi import UploadFile, HTTPException
from supabase import create_client, Client
from app.core.config import settings


class StorageService:
    """Service for managing file storage with Supabase"""

    def __init__(self):
        """Initialize Supabase client"""
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise ValueError("Supabase URL and Key must be set in environment variables")

        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket = settings.SUPABASE_BUCKET

    async def upload_file(
        self,
        file: UploadFile,
        user_id: int,
        folder: str = "uploads"
    ) -> str:
        """
        Upload file to Supabase Storage
        Returns the public URL of the uploaded file
        """
        try:
            # Generate unique filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_ext = os.path.splitext(file.filename)[1]
            file_path = f"{folder}/{user_id}/{timestamp}_{file.filename}"

            # Read file content
            file_content = await file.read()

            # Upload to Supabase
            response = self.client.storage.from_(self.bucket).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": file.content_type}
            )

            # Get public URL
            public_url = self.client.storage.from_(self.bucket).get_public_url(file_path)

            return public_url

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file: {str(e)}"
            )

    async def upload_bytes(
        self,
        file_content: bytes,
        filename: str,
        user_id: int,
        folder: str = "processed",
        content_type: str = "image/png"
    ) -> str:
        """
        Upload bytes data to Supabase Storage
        Returns the public URL of the uploaded file
        """
        try:
            # Generate unique filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_path = f"{folder}/{user_id}/{timestamp}_{filename}"

            # Upload to Supabase
            response = self.client.storage.from_(self.bucket).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": content_type}
            )

            # Get public URL
            public_url = self.client.storage.from_(self.bucket).get_public_url(file_path)

            return public_url

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload bytes: {str(e)}"
            )

    async def delete_file(self, file_url: str) -> bool:
        """
        Delete file from Supabase Storage
        Returns True if successful
        """
        try:
            # Extract file path from URL
            # Assuming URL format: https://{project}.supabase.co/storage/v1/object/public/{bucket}/{path}
            path_parts = file_url.split(f"{self.bucket}/")
            if len(path_parts) < 2:
                raise ValueError("Invalid file URL")

            file_path = path_parts[1]

            # Delete from Supabase
            response = self.client.storage.from_(self.bucket).remove([file_path])

            return True

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete file: {str(e)}"
            )

    def get_public_url(self, file_path: str) -> str:
        """Get public URL for a file path"""
        return self.client.storage.from_(self.bucket).get_public_url(file_path)

    async def download_file(self, file_url: str) -> bytes:
        """
        Download file from Supabase Storage
        Returns file content as bytes
        """
        try:
            # Extract file path from URL
            path_parts = file_url.split(f"{self.bucket}/")
            if len(path_parts) < 2:
                raise ValueError("Invalid file URL")

            file_path = path_parts[1]

            # Download from Supabase
            response = self.client.storage.from_(self.bucket).download(file_path)

            return response

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to download file: {str(e)}"
            )

    async def list_files(self, user_id: int, folder: str = "uploads") -> list[dict]:
        """
        List all files for a user in a specific folder
        Returns list of file metadata
        """
        try:
            folder_path = f"{folder}/{user_id}"

            # List files from Supabase
            response = self.client.storage.from_(self.bucket).list(folder_path)

            return response

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to list files: {str(e)}"
            )


# Singleton instance
_storage_service = None


def get_storage_service() -> StorageService:
    """Get or create StorageService singleton"""
    global _storage_service
    if _storage_service is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise ValueError("Supabase configuration not set")
        _storage_service = StorageService()
    return _storage_service
