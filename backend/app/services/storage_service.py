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


# Singleton instance
storage_service = StorageService() if settings.SUPABASE_URL and settings.SUPABASE_KEY else None
