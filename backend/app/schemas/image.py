from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.image import ImageStatus


class ImageBase(BaseModel):
    """Base schema for image"""
    pass


class ImageCreate(BaseModel):
    """Schema for creating a new image"""
    project_id: int = Field(..., description="Project ID to associate with")


class ImageRead(BaseModel):
    """Schema for reading image data"""
    id: int
    project_id: int
    original_image_url: str
    processed_image_url: Optional[str] = None
    background_image_url: Optional[str] = None
    ad_copy: Optional[str] = None
    status: ImageStatus
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ImageUploadResponse(BaseModel):
    """Schema for image upload response"""
    image_id: int
    original_image_url: str
    status: ImageStatus
    message: str
