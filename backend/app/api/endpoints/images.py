from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.database import get_async_session
from app.core.auth import current_active_user
from app.core.config import get_settings
from app.models.user import User
from app.models.image import Image
from app.models.project import Project
from app.schemas.image import ImageRead, ImageUploadResponse, CaptionGenerateRequest, CaptionGenerateResponse
# from app.services.storage_service import storage_service
# from app.services.credit_service import CreditService

router = APIRouter()
settings = get_settings()


@router.post("/upload", response_model=ImageUploadResponse, status_code=201)
async def upload_image(
    file: UploadFile = File(...),
    project_id: int = Form(...),
    style: Optional[str] = Form(None),
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Upload an image for processing
    Deducts credits and creates an image record
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )

    # Verify project exists and belongs to user
    result = await session.execute(
        select(Project).where(
            Project.id == project_id,
            Project.user_id == user.id
        )
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if user has enough credits
    credit_cost = settings.CREDIT_COSTS.get("image_generation", 1)
    if user.credits < credit_cost:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient credits. Required: {credit_cost}, Available: {user.credits}"
        )

    try:
        # TODO: Implement storage service integration
        # For now, create placeholder URL
        file_url = f"placeholder://uploads/{user.id}/{file.filename}"

        # Create image record
        db_image = Image(
            project_id=project_id,
            user_id=user.id,
            original_url=file_url,
            style=style
        )
        session.add(db_image)

        # Deduct credits (simplified - should use CreditService)
        user.credits -= credit_cost

        await session.commit()
        await session.refresh(db_image)

        return ImageUploadResponse(
            image_id=db_image.id,
            original_url=db_image.original_url,
            message="Image uploaded successfully. Processing will begin shortly."
        )

    except HTTPException:
        raise
    except Exception as e:
        # Rollback transaction on error
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload image: {str(e)}"
        )


@router.get("/", response_model=List[ImageRead])
async def list_images(
    project_id: Optional[int] = None,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
    skip: int = 0,
    limit: int = 100
):
    """List images for the current user, optionally filtered by project"""
    query = select(Image).join(Project).where(Project.user_id == user.id)

    if project_id:
        query = query.where(Image.project_id == project_id)

    query = query.offset(skip).limit(limit).order_by(Image.created_at.desc())

    result = await session.execute(query)
    images = result.scalars().all()

    return images


@router.get("/{image_id}", response_model=ImageRead)
async def get_image(
    image_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Get a specific image by ID"""
    result = await session.execute(
        select(Image)
        .join(Project)
        .where(
            Image.id == image_id,
            Project.user_id == user.id
        )
    )
    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    return image


@router.delete("/{image_id}", status_code=204)
async def delete_image(
    image_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Delete an image"""
    result = await session.execute(
        select(Image)
        .join(Project)
        .where(
            Image.id == image_id,
            Project.user_id == user.id
        )
    )
    image = result.scalar_one_or_none()

    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # TODO: Delete files from storage
    # if storage_service:
    #     await storage_service.delete_file(image.original_url)
    #     if image.processed_url:
    #         await storage_service.delete_file(image.processed_url)

    await session.delete(image)
    await session.commit()

    return None


@router.post("/caption/generate", response_model=CaptionGenerateResponse, status_code=200)
async def generate_caption(
    request: CaptionGenerateRequest,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Generate AI caption for an image
    Deducts credits for caption generation
    """
    # Verify image exists and belongs to user
    result = await session.execute(
        select(Image)
        .join(Project)
        .where(
            Image.id == request.image_id,
            Project.user_id == user.id
        )
    )
    image = result.scalar_one_or_none()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    # Check if user has enough credits
    credit_cost = settings.CREDIT_COSTS.get("caption_generation", 0.5)
    if user.credits < credit_cost:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient credits. Required: {credit_cost}, Available: {user.credits}"
        )

    try:
        # TODO: Implement AI caption generation service
        # For now, create placeholder caption
        caption = f"[AI Generated Caption] {request.tone or 'neutral'} tone, {request.length or 'medium'} length"

        caption_metadata = {
            "tone": request.tone or "neutral",
            "length": request.length or "medium",
            "include_hashtags": request.include_hashtags,
            "hashtags": ["#example", "#placeholder"] if request.include_hashtags else [],
            "generated_at": "2025-10-24T00:00:00Z"
        }

        # Update image with caption
        image.caption = caption
        image.caption_metadata = caption_metadata

        # Deduct credits
        user.credits -= credit_cost

        await session.commit()
        await session.refresh(image)

        return CaptionGenerateResponse(
            image_id=image.id,
            caption=caption,
            caption_metadata=caption_metadata,
            message="Caption generated successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate caption: {str(e)}"
        )
