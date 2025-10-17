from sqlalchemy import String, Integer, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum
from app.models.base import Base, IDMixin, TimestampMixin


class ImageStatus(str, Enum):
    """Image processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Image(Base, IDMixin, TimestampMixin):
    """Image model to store generated images and metadata"""

    __tablename__ = "images"

    # File paths/URLs
    original_image_url: Mapped[str] = mapped_column(String(512), nullable=False)
    processed_image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    background_image_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # AI generated content
    ad_copy: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Metadata
    status: Mapped[ImageStatus] = mapped_column(
        SQLEnum(ImageStatus),
        default=ImageStatus.PENDING,
        nullable=False
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Foreign key
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="images")
