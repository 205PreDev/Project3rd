from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.auth import current_active_user
from app.models.user import User
from app.schemas.credit import CreditBalance, CreditAdd, CreditTransaction
from app.services.credit_service import CreditService

router = APIRouter()


@router.get("/balance", response_model=CreditBalance)
async def get_credit_balance(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get current user's credit balance"""
    balance = await CreditService.get_balance(user.id, session)
    return CreditBalance(credits=balance)


@router.post("/add", response_model=CreditTransaction)
async def add_credits(
    credit_add: CreditAdd,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Add credits to user account
    (This would typically be called after a successful payment)
    """
    result = await CreditService.add_credits(
        user_id=user.id,
        amount=credit_add.amount,
        session=session,
        description=credit_add.description or "Credit purchase"
    )

    return CreditTransaction(**result)
