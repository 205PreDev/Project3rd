from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime, timedelta, timezone
import secrets
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.core.database import get_async_session
from app.core.config import get_settings
from app.models.trial_session import TrialSession
from app.schemas.trial import (
    TrialSessionCreate,
    TrialSessionRead,
    TrialSessionUploadResponse
)
from app.services.local_storage_service import get_local_storage
from app.services.gemini_service import get_gemini_service

router = APIRouter()
settings = get_settings()
storage = get_local_storage()

# Gemini 서비스 lazy 초기화
_gemini_instance = None
_executor = ThreadPoolExecutor(max_workers=3)

def get_gemini():
    global _gemini_instance
    if _gemini_instance is None:
        try:
            from app.services.gemini_service import get_gemini_service
            _gemini_instance = get_gemini_service()
            print("✅ Gemini service initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Gemini: {e}")
            import traceback
            traceback.print_exc()
            raise
    return _gemini_instance

async def run_in_threadpool(func, *args, **kwargs):
    """동기 함수를 비동기로 실행"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, lambda: func(*args, **kwargs))


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
        print(f"📝 Processing upload for session: {session_id}")

        # 1. 파일 로컬 저장
        print(f"💾 Saving file: {file.filename}")
        file_path = await storage.save_upload_file(file, user_id=session_id, folder="trial")
        file_url = storage.get_file_url(file_path)
        print(f"✅ File saved: {file_url}")

        # 2. Gemini로 이미지 분석
        print("🔍 Analyzing image with Gemini...")
        file.file.seek(0)  # 파일 포인터 리셋
        image_data = await file.read()
        print(f"   Image data size: {len(image_data)} bytes")

        try:
            gemini_service = get_gemini()
            print("   Gemini service obtained")

            # 동기 함수를 비동기로 실행
            print("   Calling analyze_image...")
            analysis = await run_in_threadpool(gemini_service.analyze_image, image_data)
            print(f"✅ Image analyzed: {analysis}")
        except Exception as e:
            print(f"❌ Error during image analysis: {e}")
            import traceback
            traceback.print_exc()
            raise

        # 3. 광고 문구 생성 (선택적 스타일 적용)
        print("✍️ Generating captions...")
        caption_style = style if style else "감성형"

        captions = await run_in_threadpool(
            gemini_service.generate_caption,
            product_description=analysis.get("description", "상품 이미지"),
            platform="instagram",
            style=caption_style,
            length="medium"
        )
        print(f"✅ Captions generated: {len(captions)} captions")

        # 4. 처리된 이미지 URL (현재는 원본과 동일, 추후 배경 제거 추가)
        processed_url = file_url

        # 5. 세션 생성 (expires in 24 hours)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

        trial_session = TrialSession(
            session_id=session_id,
            original_image_url=file_url,
            processed_image_url=processed_url,
            style=caption_style,
            caption=captions[0] if captions else None,  # 첫 번째 문구 저장
            expires_at=expires_at
        )

        db_session.add(trial_session)
        await db_session.commit()
        await db_session.refresh(trial_session)

        return TrialSessionUploadResponse(
            session_id=trial_session.session_id,
            original_image_url=trial_session.original_image_url,
            processed_image_url=trial_session.processed_image_url,
            caption=trial_session.caption,
            message="Trial image processed successfully. Session expires in 24 hours.",
            expires_at=trial_session.expires_at,
            analysis=analysis,  # 분석 결과 포함
            captions=captions  # 생성된 광고 문구 리스트
        )

    except HTTPException:
        await db_session.rollback()
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"ERROR in trial upload: {error_trace}")  # 콘솔에 출력
        await db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process trial image: {str(e)}\n{error_trace}"
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
