"""
Supabase Auth JWT 검증
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_async_session
from app.models.user import User


# Bearer 토큰 스키마
security = HTTPBearer()


class SupabaseAuth:
    """Supabase JWT 검증 클래스"""

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Supabase JWT 토큰 검증

        Args:
            token: JWT 토큰

        Returns:
            디코딩된 페이로드

        Raises:
            HTTPException: 토큰이 유효하지 않을 경우
        """
        if not settings.SUPABASE_KEY:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Supabase configuration not set"
            )

        try:
            # Supabase는 HS256 알고리즘 사용
            payload = jwt.decode(
                token,
                settings.SUPABASE_KEY,
                algorithms=[settings.ALGORITHM],
                options={"verify_aud": False}  # audience 검증 비활성화
            )
            return payload

        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    async def get_or_create_user(
        session: AsyncSession,
        email: str,
        provider: str = "supabase",
        provider_id: Optional[str] = None
    ) -> User:
        """
        Supabase 사용자 조회 또는 생성

        Args:
            session: 데이터베이스 세션
            email: 이메일
            provider: 인증 제공자 (기본: supabase)
            provider_id: 제공자 사용자 ID

        Returns:
            User 객체
        """
        # 기존 사용자 조회
        result = await session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if user:
            return user

        # 새 사용자 생성
        user = User(
            email=email,
            provider=provider,
            provider_id=provider_id,
            credits=10.0  # 기본 크레딧
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user


async def get_current_user_from_supabase(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_async_session)
) -> User:
    """
    Supabase JWT에서 현재 사용자 조회 (Dependency)

    Args:
        credentials: Bearer 토큰
        session: 데이터베이스 세션

    Returns:
        User 객체

    Raises:
        HTTPException: 인증 실패 시
    """
    token = credentials.credentials
    supabase_auth = SupabaseAuth()

    # JWT 검증
    payload = supabase_auth.verify_token(token)

    # 페이로드에서 이메일 추출
    email = payload.get("email")
    user_id = payload.get("sub")  # Supabase user ID

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: email not found",
        )

    # 사용자 조회 또는 생성
    user = await supabase_auth.get_or_create_user(
        session=session,
        email=email,
        provider="supabase",
        provider_id=user_id
    )

    return user


async def get_optional_user_from_supabase(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: AsyncSession = Depends(get_async_session)
) -> Optional[User]:
    """
    선택적 Supabase 인증 (게스트 허용)

    Args:
        credentials: Bearer 토큰 (선택)
        session: 데이터베이스 세션

    Returns:
        User 객체 또는 None
    """
    if not credentials:
        return None

    try:
        return await get_current_user_from_supabase(credentials, session)
    except HTTPException:
        return None
