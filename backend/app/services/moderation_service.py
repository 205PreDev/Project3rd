"""
OpenAI Moderation API 서비스
"""
from typing import Optional
import openai
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.prompt_violation import PromptViolation


class ModerationService:
    """프롬프트 검증 및 콘텐츠 조정 서비스"""

    # 금지 키워드 리스트 (한국어)
    BANNED_KEYWORDS = [
        "폭력", "혐오", "성적", "자해", "불법",
        "마약", "무기", "도박", "사기", "욕설"
    ]

    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set")
        openai.api_key = settings.OPENAI_API_KEY

    async def validate_prompt(
        self,
        prompt: str,
        user_id: int,
        session: AsyncSession
    ) -> dict:
        """
        프롬프트 유효성 검증

        Args:
            prompt: 사용자 프롬프트
            user_id: 사용자 ID
            session: 데이터베이스 세션

        Returns:
            {
                "is_valid": bool,
                "violation_type": str | None,
                "message": str,
                "flagged_keywords": list[str] | None
            }
        """
        # 1. 키워드 기반 필터링
        keyword_result = self._check_banned_keywords(prompt)
        if not keyword_result["is_valid"]:
            # 위반 기록 저장
            await self._log_violation(
                session=session,
                user_id=user_id,
                violation_type="banned_keyword",
                details={"flagged_keywords": keyword_result["flagged_keywords"]}
            )
            return keyword_result

        # 2. OpenAI Moderation API 호출
        try:
            moderation_result = await self._check_openai_moderation(prompt)
            if not moderation_result["is_valid"]:
                # 위반 기록 저장
                await self._log_violation(
                    session=session,
                    user_id=user_id,
                    violation_type=moderation_result["violation_type"],
                    details={"api_response": moderation_result}
                )
            return moderation_result

        except Exception as e:
            # API 실패 시 키워드 필터링 결과만 사용
            print(f"Moderation API error: {str(e)}")
            return {
                "is_valid": True,
                "violation_type": None,
                "message": "Prompt validated (API unavailable)",
                "flagged_keywords": None
            }

    def _check_banned_keywords(self, prompt: str) -> dict:
        """
        금지 키워드 확인

        Args:
            prompt: 프롬프트 텍스트

        Returns:
            검증 결과
        """
        prompt_lower = prompt.lower()
        flagged = [kw for kw in self.BANNED_KEYWORDS if kw in prompt_lower]

        if flagged:
            return {
                "is_valid": False,
                "violation_type": "banned_keyword",
                "message": f"Prompt contains banned keywords: {', '.join(flagged)}",
                "flagged_keywords": flagged
            }

        return {
            "is_valid": True,
            "violation_type": None,
            "message": "No banned keywords found",
            "flagged_keywords": None
        }

    async def _check_openai_moderation(self, prompt: str) -> dict:
        """
        OpenAI Moderation API 호출

        Args:
            prompt: 프롬프트 텍스트

        Returns:
            검증 결과
        """
        try:
            response = await openai.Moderation.acreate(input=prompt)
            result = response["results"][0]

            if result["flagged"]:
                # 위반 카테고리 찾기
                categories = result["categories"]
                flagged_categories = [
                    cat for cat, flagged in categories.items() if flagged
                ]

                return {
                    "is_valid": False,
                    "violation_type": "openai_moderation",
                    "message": f"Content flagged for: {', '.join(flagged_categories)}",
                    "flagged_keywords": flagged_categories
                }

            return {
                "is_valid": True,
                "violation_type": None,
                "message": "Prompt passed moderation",
                "flagged_keywords": None
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Moderation API error: {str(e)}"
            )

    async def _log_violation(
        self,
        session: AsyncSession,
        user_id: int,
        violation_type: str,
        details: Optional[dict] = None
    ):
        """
        프롬프트 위반 로그 저장

        Args:
            session: 데이터베이스 세션
            user_id: 사용자 ID
            violation_type: 위반 유형
            details: 위반 상세 정보
        """
        violation = PromptViolation(
            user_id=user_id,
            violation_type=violation_type,
            details=details
        )
        session.add(violation)
        await session.commit()

    async def get_user_violations(
        self,
        session: AsyncSession,
        user_id: int,
        limit: int = 10
    ) -> list[PromptViolation]:
        """
        사용자 위반 내역 조회

        Args:
            session: 데이터베이스 세션
            user_id: 사용자 ID
            limit: 조회 제한

        Returns:
            위반 내역 리스트
        """
        result = await session.execute(
            select(PromptViolation)
            .where(PromptViolation.user_id == user_id)
            .order_by(PromptViolation.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()


# 싱글톤 인스턴스
_moderation_service: Optional[ModerationService] = None


def get_moderation_service() -> ModerationService:
    """ModerationService 싱글톤 인스턴스 반환"""
    global _moderation_service
    if _moderation_service is None:
        _moderation_service = ModerationService()
    return _moderation_service
