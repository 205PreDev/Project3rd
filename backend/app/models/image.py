"""
이미지 모델
"""
from sqlalchemy import String, Integer, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, Dict, Any

from app.models.base import Base, IDMixin, TimestampMixin


class Image(Base, IDMixin, TimestampMixin):
    """이미지 테이블 - 생성된 이미지 저장"""
    __tablename__ = "images"

    # Foreign keys
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # 파일 경로 (Supabase Storage URLs)
    original_url: Mapped[str] = mapped_column(Text, nullable=False)  # 원본 이미지
    processed_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 처리된 이미지 (배경 제거 + 합성)

    # 배경 스타일
    style: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # 'clean_white', 'luxury_marble', etc.

    # AI 생성 광고 문구
    caption: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    caption_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)  # {type: 'recommended', length: 245, hashtags: [...]}

    # 품질 점수
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="images")
    user: Mapped["User"] = relationship("User", back_populates="images")

    def __repr__(self):
        return f"<Image(id={self.id}, project_id={self.project_id}, style={self.style})>"
