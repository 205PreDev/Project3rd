from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class PromptValidationRequest(BaseModel):
    """Schema for prompt validation request"""
    prompt: str = Field(..., min_length=1, max_length=2000, description="User prompt to validate")


class PromptValidationResponse(BaseModel):
    """Schema for prompt validation response"""
    is_valid: bool
    violation_type: Optional[str] = None
    message: str
    flagged_keywords: Optional[list[str]] = None


class PromptViolationRead(BaseModel):
    """Schema for reading prompt violation logs"""
    id: int
    user_id: int
    violation_type: str
    details: Optional[Dict[str, Any]] = None
    created_at: str

    class Config:
        from_attributes = True
