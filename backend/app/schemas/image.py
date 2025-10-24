from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ImageBase(BaseModel):
    """Base schema for image"""
    style: Optional[str] = Field(None, description="Background style")
    caption: Optional[str] = Field(None, description="AI generated caption")


class ImageCreate(BaseModel):
    """Schema for creating a new image"""
    project_id: int = Field(..., description="Project ID to associate with")
    style: Optional[str] = Field(None, description="Background style preference")


class ImageRead(BaseModel):
    """Schema for reading image data"""
    id: int
    project_id: int
    user_id: int
    original_url: str
    processed_url: Optional[str] = None
    style: Optional[str] = None
    caption: Optional[str] = None
    caption_metadata: Optional[Dict[str, Any]] = None
    quality_score: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ImageUploadResponse(BaseModel):
    """Schema for image upload response"""
    image_id: int
    original_url: str
    message: str


class CaptionGenerateRequest(BaseModel):
    """Schema for caption generation request"""
    image_id: int
    tone: Optional[str] = Field(None, description="Tone: 'formal', 'casual', 'friendly'")
    length: Optional[str] = Field(None, description="Length: 'short', 'medium', 'long'")
    include_hashtags: bool = Field(True, description="Include hashtags in caption")


class CaptionGenerateResponse(BaseModel):
    """Schema for caption generation response"""
    image_id: int
    caption: str
    caption_metadata: Dict[str, Any]
    message: str
