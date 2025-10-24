from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.models.credit_transaction import CreditTransaction
from fastapi import HTTPException
from typing import Optional


class CreditService:
    """Service for managing user credits"""

    @staticmethod
    async def get_balance(user_id: int, session: AsyncSession) -> float:
        """Get user's current credit balance"""
        result = await session.execute(
            select(User.credits).where(User.id == user_id)
        )
        credits = result.scalar_one_or_none()
        if credits is None:
            raise HTTPException(status_code=404, detail="User not found")
        return credits

    @staticmethod
    async def deduct_credits(
        user_id: int,
        amount: float,
        session: AsyncSession,
        description: str = "Credit deduction",
        reason: str = "deduction",
        reference_id: Optional[int] = None
    ) -> dict:
        """
        Deduct credits from user account
        Returns new balance and success status
        """
        # Get user
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if user has enough credits
        if user.credits < amount:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient credits. Required: {amount}, Available: {user.credits}"
            )

        # Deduct credits
        user.credits -= amount

        # Create transaction record
        transaction = CreditTransaction(
            user_id=user_id,
            amount=-amount,  # Negative for deduction
            reason=reason,
            reference_id=reference_id
        )
        session.add(transaction)

        await session.commit()
        await session.refresh(user)

        return {
            "success": True,
            "new_balance": user.credits,
            "message": f"Successfully deducted {amount} credits. {description}"
        }

    @staticmethod
    async def add_credits(
        user_id: int,
        amount: float,
        session: AsyncSession,
        description: str = "Credit addition",
        reason: str = "addition",
        reference_id: Optional[int] = None
    ) -> dict:
        """
        Add credits to user account
        Returns new balance and success status
        """
        # Get user
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Add credits
        user.credits += amount

        # Create transaction record
        transaction = CreditTransaction(
            user_id=user_id,
            amount=amount,  # Positive for addition
            reason=reason,
            reference_id=reference_id
        )
        session.add(transaction)

        await session.commit()
        await session.refresh(user)

        return {
            "success": True,
            "new_balance": user.credits,
            "message": f"Successfully added {amount} credits. {description}"
        }

    @staticmethod
    async def refund_credits(
        user_id: int,
        amount: float,
        session: AsyncSession,
        reason: str = "Refund"
    ) -> dict:
        """
        Refund credits to user account (e.g., when AI processing fails)
        """
        return await CreditService.add_credits(
            user_id=user_id,
            amount=amount,
            session=session,
            description=f"Refund: {reason}",
            reason="refund"
        )

    @staticmethod
    async def get_transaction_history(
        user_id: int,
        session: AsyncSession,
        limit: int = 50
    ) -> list[CreditTransaction]:
        """
        Get credit transaction history for a user
        Returns list of transactions (most recent first)
        """
        result = await session.execute(
            select(CreditTransaction)
            .where(CreditTransaction.user_id == user_id)
            .order_by(CreditTransaction.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def has_sufficient_credits(
        user_id: int,
        required_amount: float,
        session: AsyncSession
    ) -> bool:
        """
        Check if user has sufficient credits
        """
        try:
            balance = await CreditService.get_balance(user_id, session)
            return balance >= required_amount
        except HTTPException:
            return False


# Credit costs constants
CREDIT_COSTS = {
    "image_generation": 1.0,
    "caption_generation": 0.3,
    "background_removal": 0.5,
}

# Bonus credits
CREDIT_BONUSES = {
    "welcome_bonus": 10.0,
    "referral_bonus": 5.0,
    "first_share": 2.0,
}
