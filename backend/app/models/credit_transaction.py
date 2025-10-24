"""
크레딧 거래 모델
"""
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from app.models.base import Base, IDMixin, TimestampMixin


class CreditTransaction(Base, IDMixin, TimestampMixin):
    """크레딧 거래 내역 테이블"""
    __tablename__ = "credit_transactions"

    # Foreign key
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # 거래 정보
    amount: Mapped[int] = mapped_column(Integer, nullable=False)  # 양수: 충전, 음수: 차감
    reason: Mapped[str] = mapped_column(String(100), nullable=False)  # 'welcome_bonus', 'image_generation', etc.
    reference_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 관련 이미지 ID 등

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="credit_transactions")

    def __repr__(self):
        return f"<CreditTransaction(id={self.id}, user_id={self.user_id}, amount={self.amount}, reason={self.reason})>"
