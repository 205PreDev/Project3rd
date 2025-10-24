from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime


class TrialSessionCreate(BaseModel):
    """Schema for creating a trial session (non-authenticated users)"""
    style: Optional[str] = Field(None, description="Background style preference")


class TrialSessionRead(BaseModel):
    """Schema for reading trial session data"""
    session_id: str
    original_image_url: str
    processed_image_url: Optional[str] = None
    style: Optional[str] = None
    caption: Optional[str] = None
    quality_score: Optional[float] = None
    expires_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrialSessionUploadResponse(BaseModel):
    """Schema for trial session upload response"""
    session_id: str
    original_image_url: str
    processed_image_url: Optional[str] = None
    caption: Optional[str] = None
    message: str
    expires_at: datetime
    analysis: Optional[Dict] = Field(None, description="Image analysis result from Gemini")
    captions: Optional[List[str]] = Field(None, description="Generated ad captions")
