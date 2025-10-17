from fastapi_users import schemas
from typing import Optional


class UserRead(schemas.BaseUser[int]):
    """Schema for reading user data"""
    full_name: Optional[str] = None
    credits: float


class UserCreate(schemas.BaseUserCreate):
    """Schema for creating a new user"""
    full_name: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating user data"""
    full_name: Optional[str] = None
