from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from fastapi import HTTPException


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
        description: str = "Credit deduction"
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
        description: str = "Credit addition"
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
            description=f"Refund: {reason}"
        )


# Credit costs constants
CREDIT_COSTS = {
    "image_generation": 1.0,
    "text_generation": 0.5,
    "background_removal": 0.5,
}
