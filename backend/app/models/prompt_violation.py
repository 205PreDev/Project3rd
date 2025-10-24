"""
프롬프트 위반 모델
"""
from sqlalchemy import String, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, Dict, Any

from app.models.base import Base, IDMixin, TimestampMixin


class PromptViolation(Base, IDMixin, TimestampMixin):
    """프롬프트 위반 로그 테이블"""
    __tablename__ = "prompt_violations"

    # Foreign key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # 위반 정보
    violation_type: Mapped[str] = mapped_column(String(50), nullable=False)  # 'banned_keyword', 'openai_moderation', etc.
    details: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # 위반 상세 정보

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="prompt_violations")

    def __repr__(self):
        return f"<PromptViolation(id={self.id}, user_id={self.user_id}, type={self.violation_type})>"
