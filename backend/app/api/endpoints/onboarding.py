from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from app.core.database import get_async_session
from app.core.auth import current_active_user
from app.models.user import User
from app.models.onboarding_progress import OnboardingProgress
from app.schemas.onboarding import (
    OnboardingProgressRead,
    OnboardingProgressUpdate,
    OnboardingChecklistItem
)

router = APIRouter()


@router.get("/progress", response_model=OnboardingProgressRead)
async def get_onboarding_progress(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get current user's onboarding progress"""
    result = await session.execute(
        select(OnboardingProgress).where(OnboardingProgress.user_id == user.id)
    )
    progress = result.scalar_one_or_none()

    if not progress:
        # Create initial progress if it doesn't exist
        progress = OnboardingProgress(
            user_id=user.id,
            stage="landing",
            tutorial_step=None,
            checklist={}
        )
        session.add(progress)
        await session.commit()
        await session.refresh(progress)

    return progress


@router.patch("/progress", response_model=OnboardingProgressRead)
async def update_onboarding_progress(
    update: OnboardingProgressUpdate,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Update onboarding progress"""
    result = await session.execute(
        select(OnboardingProgress).where(OnboardingProgress.user_id == user.id)
    )
    progress = result.scalar_one_or_none()

    if not progress:
        raise HTTPException(status_code=404, detail="Onboarding progress not found")

    # Update fields
    if update.stage is not None:
        progress.stage = update.stage

    if update.tutorial_step is not None:
        progress.tutorial_step = update.tutorial_step

    if update.checklist is not None:
        progress.checklist = update.checklist

    if update.completed:
        progress.completed_at = datetime.now(timezone.utc)

    await session.commit()
    await session.refresh(progress)

    return progress


@router.post("/checklist", response_model=OnboardingProgressRead)
async def update_checklist_item(
    item: OnboardingChecklistItem,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Update a single checklist item"""
    result = await session.execute(
        select(OnboardingProgress).where(OnboardingProgress.user_id == user.id)
    )
    progress = result.scalar_one_or_none()

    if not progress:
        raise HTTPException(status_code=404, detail="Onboarding progress not found")

    # Update specific checklist item
    if progress.checklist is None:
        progress.checklist = {}

    progress.checklist[item.item_key] = item.completed

    await session.commit()
    await session.refresh(progress)

    return progress
