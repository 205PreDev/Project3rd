from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class OnboardingProgressRead(BaseModel):
    """Schema for reading onboarding progress"""
    user_id: int
    stage: str = Field(..., description="Current stage: 'landing', 'trial', 'signup', 'tutorial', 'dashboard'")
    tutorial_step: Optional[int] = Field(None, description="Tutorial step: 1, 2, 3")
    checklist: Dict[str, Any] = Field(default_factory=dict, description="Progress checklist")
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OnboardingProgressUpdate(BaseModel):
    """Schema for updating onboarding progress"""
    stage: Optional[str] = Field(None, description="Update current stage")
    tutorial_step: Optional[int] = Field(None, description="Update tutorial step")
    checklist: Optional[Dict[str, Any]] = Field(None, description="Update checklist")
    completed: bool = Field(False, description="Mark onboarding as completed")


class OnboardingChecklistItem(BaseModel):
    """Schema for updating a single checklist item"""
    item_key: str = Field(..., description="Checklist item key (e.g., 'project_created')")
    completed: bool = Field(..., description="Whether the item is completed")
