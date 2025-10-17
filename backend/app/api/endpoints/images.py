from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.core.database import get_async_session
from app.core.auth import current_active_user
from app.models.user import User
from app.models.image import Image, ImageStatus
from app.models.project import Project
from app.schemas.image import ImageRead, ImageUploadResponse
from app.services.storage_service import storage_service
from app.services.credit_service import CreditService, CREDIT_COSTS

router = APIRouter()


@router.post("/upload", response_model=ImageUploadResponse, status_code=201)
async def upload_image(
    file: UploadFile = File(...),
    project_id: int = Form(...),
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
    credit_cost = CREDIT_COSTS["image_generation"]
    if user.credits < credit_cost:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient credits. Required: {credit_cost}, Available: {user.credits}"
        )

    try:
        # Upload file to storage
        if not storage_service:
            raise HTTPException(
                status_code=500,
                detail="Storage service not configured. Please set SUPABASE_URL and SUPABASE_KEY"
            )

        file_url = await storage_service.upload_file(
            file=file,
            user_id=user.id,
            folder="uploads"
        )

        # Create image record
        db_image = Image(
            project_id=project_id,
            original_image_url=file_url,
            status=ImageStatus.PENDING
        )
        session.add(db_image)

        # Deduct credits
        await CreditService.deduct_credits(
            user_id=user.id,
            amount=credit_cost,
            session=session,
            description=f"Image upload - {file.filename}"
        )

        await session.commit()
        await session.refresh(db_image)

        return ImageUploadResponse(
            image_id=db_image.id,
            original_image_url=db_image.original_image_url,
            status=db_image.status,
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
    #     await storage_service.delete_file(image.original_image_url)
    #     if image.processed_image_url:
    #         await storage_service.delete_file(image.processed_image_url)

    await session.delete(image)
    await session.commit()

    return None
