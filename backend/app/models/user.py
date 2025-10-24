"""
사용자 모델
"""
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

from app.models.base import Base, IDMixin, TimestampMixin


class User(Base, IDMixin, TimestampMixin):
    """사용자 테이블"""
    __tablename__ = "users"

    # 기본 정보
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # 소셜 로그인 시 NULL

    # 소셜 로그인
    provider: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # 'email', 'google', 'kakao', 'naver'
    provider_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)

    # 크레딧
    credits: Mapped[float] = mapped_column(Float, default=10.0, nullable=False)  # 가입 시 10 크레딧

    # Relationships
    projects: Mapped[List["Project"]] = relationship(
        "Project",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    images: Mapped[List["Image"]] = relationship(
        "Image",
        back_populates="user"
    )
    credit_transactions: Mapped[List["CreditTransaction"]] = relationship(
        "CreditTransaction",
        back_populates="user"
    )
    onboarding_progress: Mapped[Optional["OnboardingProgress"]] = relationship(
        "OnboardingProgress",
        back_populates="user",
        uselist=False
    )
    prompt_violations: Mapped[List["PromptViolation"]] = relationship(
        "PromptViolation",
        back_populates="user"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, credits={self.credits})>"
