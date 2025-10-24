from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime, timedelta, timezone
import secrets

from app.core.database import get_async_session
from app.core.config import get_settings
from app.models.trial_session import TrialSession
from app.schemas.trial import (
    TrialSessionCreate,
    TrialSessionRead,
    TrialSessionUploadResponse
)

router = APIRouter()
settings = get_settings()


@router.post("/upload", response_model=TrialSessionUploadResponse, status_code=201)
async def upload_trial_image(
    file: UploadFile = File(...),
    style: Optional[str] = Form(None),
    db_session: AsyncSession = Depends(get_async_session)
):
    """
    Upload an image for trial (non-authenticated users)
    Creates a temporary session that expires in 24 hours
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )

    try:
        # Generate unique session ID
        session_id = secrets.token_urlsafe(32)

        # TODO: Implement storage service integration
        # For now, create placeholder URL
        file_url = f"placeholder://trial/{session_id}/{file.filename}"

        # Create trial session (expires in 24 hours)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

        trial_session = TrialSession(
            session_id=session_id,
            original_image_url=file_url,
            style=style,
            expires_at=expires_at
        )

        db_session.add(trial_session)
        await db_session.commit()
        await db_session.refresh(trial_session)

        return TrialSessionUploadResponse(
            session_id=trial_session.session_id,
            original_image_url=trial_session.original_image_url,
            message="Trial image uploaded successfully. Session expires in 24 hours.",
            expires_at=trial_session.expires_at
        )

    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload trial image: {str(e)}"
        )


@router.get("/{session_id}", response_model=TrialSessionRead)
async def get_trial_session(
    session_id: str,
    db_session: AsyncSession = Depends(get_async_session)
):
    """Get trial session by session_id"""
    result = await db_session.execute(
        select(TrialSession).where(TrialSession.session_id == session_id)
    )
    trial_session = result.scalar_one_or_none()

    if not trial_session:
        raise HTTPException(status_code=404, detail="Trial session not found")

    # Check if session is expired
    if trial_session.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=410, detail="Trial session has expired")

    return trial_session


@router.delete("/{session_id}", status_code=204)
async def delete_trial_session(
    session_id: str,
    db_session: AsyncSession = Depends(get_async_session)
):
    """Delete trial session"""
    result = await db_session.execute(
        select(TrialSession).where(TrialSession.session_id == session_id)
    )
    trial_session = result.scalar_one_or_none()

    if not trial_session:
        raise HTTPException(status_code=404, detail="Trial session not found")

    # TODO: Delete files from storage
    # if storage_service:
    #     await storage_service.delete_file(trial_session.original_image_url)
    #     if trial_session.processed_image_url:
    #         await storage_service.delete_file(trial_session.processed_image_url)

    await db_session.delete(trial_session)
    await db_session.commit()

    return None
