from pydantic import BaseModel, Field
from typing import Optional


class CreditBalance(BaseModel):
    """Schema for reading user's credit balance"""
    credits: float = Field(..., description="Current credit balance")


class CreditDeduct(BaseModel):
    """Schema for deducting credits"""
    amount: float = Field(..., gt=0, description="Amount of credits to deduct")
    description: Optional[str] = Field(None, description="Description of the transaction")


class CreditAdd(BaseModel):
    """Schema for adding credits"""
    amount: float = Field(..., gt=0, description="Amount of credits to add")
    description: Optional[str] = Field(None, description="Description of the transaction")


class CreditTransaction(BaseModel):
    """Schema for credit transaction response"""
    success: bool
    new_balance: float
    message: str
