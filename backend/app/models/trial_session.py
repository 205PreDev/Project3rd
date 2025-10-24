"""
체험 세션 모델 (비회원 사용자용)
"""
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Text, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.models.base import Base, TimestampMixin


class TrialSession(Base, TimestampMixin):
    """체험 세션 테이블 - 비회원 사용자 임시 저장"""
    __tablename__ = "trial_sessions"

    # Primary Key (session_id)
    session_id: Mapped[str] = mapped_column(String(64), primary_key=True)

    # 이미지 정보
    original_image_url: Mapped[str] = mapped_column(Text, nullable=False)
    processed_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 배경 스타일
    style: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # AI 생성 문구
    caption: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 품질 점수
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # 만료 시간
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # 24시간 후

    # 전환 여부
    converted_to_user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    def __repr__(self):
        return f"<TrialSession(session_id={self.session_id}, expires_at={self.expires_at})>"
