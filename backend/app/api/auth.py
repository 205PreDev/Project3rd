from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.auth import auth_backend, fastapi_users
from app.core.supabase_auth import get_current_user_from_supabase
from app.core.database import get_async_session
from app.schemas.user import UserRead, UserCreate, UserUpdate
from app.models.user import User

router = APIRouter()

# Include authentication routes
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)

# Include registration route
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

# Include user management routes (get current user, update, delete)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
)

# Include password reset routes
router.include_router(
    fastapi_users.get_reset_password_router(),
)

# Include email verification routes
router.include_router(
    fastapi_users.get_verify_router(UserRead),
)


# Supabase 소셜 로그인 스키마
class SocialLoginRequest(BaseModel):
    """소셜 로그인 요청"""
    email: str
    provider: str  # 'google', 'kakao', 'naver'
    provider_id: str


class SocialLoginResponse(BaseModel):
    """소셜 로그인 응답"""
    user: UserRead
    access_token: str
    token_type: str = "bearer"


@router.post("/social-login", response_model=UserRead)
async def social_login(
    request: SocialLoginRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    소셜 로그인 (Google, Kakao, Naver)
    Supabase Auth와 연동
    """
    from app.core.supabase_auth import SupabaseAuth

    supabase_auth = SupabaseAuth()

    # 사용자 조회 또는 생성
    user = await supabase_auth.get_or_create_user(
        session=session,
        email=request.email,
        provider=request.provider,
        provider_id=request.provider_id
    )

    return user


@router.get("/me", response_model=UserRead)
async def get_current_user_supabase(
    user: User = Depends(get_current_user_from_supabase)
):
    """
    Supabase JWT로 현재 사용자 조회
    """
    return user
