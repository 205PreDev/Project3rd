"""
온보딩 진행률 모델
"""
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, Dict, Any

from app.models.base import Base, TimestampMixin


class OnboardingProgress(Base, TimestampMixin):
    """온보딩 진행률 테이블"""
    __tablename__ = "onboarding_progress"

    # Primary Key (user_id)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )

    # 진행 상태
    stage: Mapped[str] = mapped_column(String(20), nullable=False)  # 'landing', 'trial', 'signup', 'tutorial', 'dashboard'
    tutorial_step: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 1, 2, 3

    # 체크리스트 (JSON)
    checklist: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict  # {project_created: False, image_generated: False, ...}
    )

    # 완료 시간
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="onboarding_progress")

    def __repr__(self):
        return f"<OnboardingProgress(user_id={self.user_id}, stage={self.stage}, step={self.tutorial_step})>"
