from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.core.database import get_async_session
from app.core.auth import current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.prompt_violation import PromptViolation
from app.schemas.prompt import (
    PromptValidationRequest,
    PromptValidationResponse,
    PromptViolationRead
)
from app.services.moderation_service import get_moderation_service

router = APIRouter()


@router.post("/validate", response_model=PromptValidationResponse)
async def validate_prompt(
    request: PromptValidationRequest,
    user: Optional[User] = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Validate user prompt against banned keywords and OpenAI Moderation API
    Returns validation result and logs violations if any
    """
    # 게스트 사용자는 user_id = 0으로 처리
    user_id = user.id if user else 0

    # Moderation Service 호출
    moderation_service = get_moderation_service()
    result = await moderation_service.validate_prompt(
        prompt=request.prompt,
        user_id=user_id,
        session=session
    )

    return PromptValidationResponse(**result)


@router.get("/violations", response_model=list[PromptViolationRead])
async def get_user_violations(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
    limit: int = 10
):
    """
    Get current user's prompt violation history
    (For admin/debugging purposes)
    """
    moderation_service = get_moderation_service()
    violations = await moderation_service.get_user_violations(
        session=session,
        user_id=user.id,
        limit=limit
    )

    return violations
